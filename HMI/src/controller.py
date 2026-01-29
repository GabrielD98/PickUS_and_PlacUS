import struct
import threading

from storage import Storage
from communication import Communication
from data import Position, Command, CommandId, ControllerState, MachineState




class Controller:
	
	def __init__(self):
		self.storage = Storage() # mutex on Storage?
		self.com = Communication()
		self.commands = list() #probably need a mutex
		self.lastCommand = None
		self.jogVelocity = 0 #mutex
		self.controllerState = ControllerState.IDLE #mutex
		self.latestMachineInfo = (MachineState.DISCONNECTED, Position(0,0,0,0)) #mutex
		self.closeEvent = threading.Event()


	def _sendCommand(self, command:Command):
		p = command.position

		if(p is None):
			p = Position(0,0,0,0)

		byteBuffer = struct.pack('<Bfffff',
						    command.commandId,
							command.velocity, 
							p.x, p.y, p.z, p.yaw)

		self.com.sendData(byteBuffer)
	
	def _updateMachineInfo(self):
		"""Receive a machine info packet and update `latestMachineInfo`.

		Expected packet format (little-endian):
		  uint8_t machine_state
		  float32 x, y, z, yaw
		"""
		bytesBuffer = self.com.receiveData()
		format = '<Bffff'
		size = struct.calcsize(format)

		machineState, x, y, z, yaw = struct.unpack(format, bytesBuffer[:size])

		self.latestMachineInfo = (MachineState(machineState), Position(x, y, z, yaw))

	def jog(self, position:Position):
		commandToSend = Command(CommandId.MOVE, self.jogVelocity, position)
		self.commands.append(commandToSend)
	
	def setJogVelocity(self, velocity:float):
		self.jogVelocity = velocity

	def goHome(self):
		commandToSend = Command(CommandId.HOME, self.jogVelocity, None)
		self.commands.append(commandToSend)

	def stop(self):
		self.commands.insert(0,Command(CommandId.STOP,0, None))

	def start(self, commands:list):
		self.commands.extend(commands)

	def connectionToMachine(self,comPort:str):
		self.com.open(comPort)
		#startTheThread here

	def disconnectionFromMachine(self):
		pass
		#we close the port and the thread here

	def nextCommand(self) -> Command:
		self.lastCommand = self.commands[0]
		return self.commands.pop(0)

	def getLatestMachineInfo(self):
		#probably require a mutex
		return self.latestMachineInfo

	def heartBeat(self):
		while not self.closeEvent.is_set():
			commandToSend = Command(CommandId.EMPTY,0, None, None)

			match self.controllerState:
				case ControllerState.IDLE:
					pass
				
				case ControllerState.RUNNING:
					pass

				case ControllerState.MANUAL:
					pass

				case ControllerState.PAUSE:
					pass

				case ControllerState.DONE:
					pass

			self._sendCommand(commandToSend)
			self._updateMachineInfo()
			self.closeEvent.wait(timeout=0.05)



	