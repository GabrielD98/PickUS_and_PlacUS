import struct

import serial


MAGIC_NUMBER = 0xFACE


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

	def _checksum(self, data: bytes) -> int:
		return sum(data) & 0xFFFF

	def _readExact(self, size: int) -> bytes | None:
		if self.ser is None:
			return None

		buffer = bytearray()
		while len(buffer) < size:
			chunk = self.ser.read(size - len(buffer))
			if not chunk:
				return None
			buffer.extend(chunk)
		return bytes(buffer)

	def _readHeader(self) -> tuple[int, int, int] | None:
		if self.ser is None:
			return None

		magicBytes = struct.pack('<H', MAGIC_NUMBER)
		window = bytearray()
		discarded = 0

		while True:
			chunk = self.ser.read(1)
			if not chunk:
				return None

			window.append(chunk[0])
			if len(window) > 2:
				window.pop(0)
				discarded += 1

			if len(window) == 2 and bytes(window) == magicBytes:
				break

		remaining = self._readExact(4)
		if remaining is None:
			return None

		checksum, payload_size = struct.unpack('<HH', remaining)
		return MAGIC_NUMBER, checksum, payload_size

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