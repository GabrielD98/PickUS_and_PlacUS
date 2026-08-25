import struct

import serial


MAGIC_NUMBER = 0xFACE
MAX_PAYLOAD_SIZE = 256


class Communication:
	"""
	Implementation of a serial communication interface for UART communication.

	Attributes:
		port (str):
			serial port name
		baudrate (int):
			communication speed in bits per second
		ser (serial.Serial):
			serial port object

	"""

	def __init__(self, port: str, baudrate: int):
		self.port = port
		self.baudrate = baudrate
		self.ser = None
		self._window = bytearray(2)
		self._windowReady = False
		self._aligned     = False

	def _checksum(self, data: bytes) -> int:
		return sum(data) & 0xFFFF

	def _readExact(self, size: int) -> bytes | None:
		if self.ser is None:
			return None

		if(self.ser.in_waiting >= size):
			buffer = bytearray()
			while len(buffer) < size:
				chunk = self.ser.read(size - len(buffer))
				if not chunk:
					return None
				buffer.extend(chunk)
			return bytes(buffer)
		else:
			return None


	def _readHeader(self) -> tuple[int, int, int] | None:
		if self.ser is None:
			return None

		result = None

		# Prime only if window isn't already loaded from a previous attempt
		if not self._windowReady and not self._aligned:
			initial = self._readExact(2)
			if initial is not None:
				self._window[0] = initial[0]
				self._window[1] = initial[1]
				self._windowReady = True

		if self._windowReady and not self._aligned:
			magicBytes = struct.pack('<H', MAGIC_NUMBER)

			while not self._aligned:
				if bytes(self._window) == magicBytes:
					self._aligned = True
				else:
					next_byte = self._readExact(1)
					if next_byte is not None:
						self._window[0] = self._window[1]
						self._window[1] = next_byte[0]
					else:
						break  # window preserved, retry next call

		if self._aligned:
			remaining = self._readExact(4)
			if remaining is not None:
				checksum, payload_size = struct.unpack('<HH', remaining)
				if payload_size < MAX_PAYLOAD_SIZE:
					result = (MAGIC_NUMBER, checksum, payload_size)
				# Reset fully for next header
				self._windowReady = False
				self._aligned     = False

		return result

	def open(self):
		"""Open the serial port."""
		self.ser = serial.Serial(
			port=self.port,
			baudrate=self.baudrate,
			timeout=1,
		)

		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()

	def close(self):
		"""Close the serial port if it is open."""
		if self.isPortOpen():
			self.ser.close()
		return

	def sendData(self, data: bytes):
		"""Send data through the serial port.

		Parameters:
			data (bytes):
				Data to send
		"""
		if self.isPortOpen():
			try:
				payload = bytes(data)
				header = struct.pack('<HHH', MAGIC_NUMBER, self._checksum(payload), len(payload))
				self.ser.write(header)
				self.ser.write(payload)
			except serial.SerialException:
				pass
		return

	def receiveData(self, numBytes: int) -> bytes | None:
		"""Read and validate a framed packet from the serial port.

		Parameters:
			numBytes (int):
				Minimum payload size expected by the caller.

		Returns:
			bytes: The validated payload bytes.
			None: if the frame is invalid, too small, or the port is not open.
		"""
		if self.isPortOpen():
			try:
				header = self._readHeader()
				if header is None:
					return None

				magicNumber, checksum, payload_size = header
				payload = self._readExact(payload_size)
				if payload is None:
					return None


				if self._checksum(payload) != checksum:
					return None

				if numBytes > 0 and len(payload) < numBytes:
					return None

				data = payload
			except (serial.SerialException, AttributeError):
				data = None
		else:
			data = None
		return data
		
	def isPortOpen(self) -> bool:
		"""
        Tell if the port is open

		Returns:
			bool: True if the port is open, False if close or not init
        """
		result = False

		if self.ser is not None:
			result = self.ser.is_open

		return result