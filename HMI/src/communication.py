import serial

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

	def __init__(self, port:str, baudrate:int):
		self.port = port
		self.baudrate = baudrate
		self.ser = None

	
	def open(self):
		"""Open the serial port."""
		self.ser = serial.Serial(
			port=self.port,
			baudrate=self.baudrate,
			timeout=None,
		)
		# Flush buffers to clear any startup messages or leftover data
		self.ser.reset_input_buffer()
		self.ser.reset_output_buffer()


	def close(self):
		"""Close the serial port if it is open.
		"""
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
			self.ser.write(data)
		return

	def receiveData(self, numBytes: int) -> bytes:
		"""Read a fixed number of bytes from the serial port (blocking).

		Parameters:
			numBytes (int):
				Number of bytes to read

		Returns:
			bytes: The raw bytes read.
		"""
		if self.isPortOpen():
			data = self.ser.read(numBytes)
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