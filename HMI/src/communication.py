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


	def close(self):
		"""Close the serial port if it is open.
		"""
		if self.isPortOpen():
			self.ser.close()


	def sendRequest(self, request: bytes):
		"""Send data through the serial port.

		Parameters:
			request (bytes):
				Data to send
        """
		if self.isPortOpen():
			self.ser.write(request)
		return

	def receiveRequest(self) -> bytes:
		"""Read a line from the serial port (blocking until '\\n').

		Returns:
			bytes: The raw bytes read, including the terminating newline if present.
		"""
		if self.isPortOpen():
			data = self.ser.readline()
		else:
			data = None
		return data
		
	def isPortOpen(self) -> bool:
		"""
        Tell if the port is open
        """
		result = False

		if self.ser is not None:
			result = self.ser.is_open
			
		return result