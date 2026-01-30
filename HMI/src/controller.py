import struct
import threading

from storage import Storage
from communication import Communication
from data import Position, Command, CommandId, ControllerState, MachineState, TransitionRequest




class Controller:
	
	def __init__(self):
		self.storage = Storage() # mutex on Storage?
		self.com = Communication()
		self.commands = list() #probably need a mutex
		self.lastCommand = Command(CommandId.EMPTY,0, None, None)
		self.jogVelocity = 0 #mutex
		self.controllerState = ControllerState.IDLE #mutex
		self.latestMachineInfo = (MachineState.DISCONNECTED, Position(0,0,0,0)) #mutex
		self.closeEvent = threading.Event()
		self.comThread = None
		self.controllerRequestTransitionField = 0


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

	def _nextCommand(self) -> Command:
		nextCommand = None
		if self.commands:
			nextCommand = self.commands.pop(0)
			self.lastCommand = nextCommand
		return nextCommand
	
	def _toggleRequestTransitionBit(self, bit: TransitionRequest, state: bool):
		if state:
			self.controllerRequestTransitionField |= bit
		else:
			self.controllerRequestTransitionField &= ~bit
	
	def _check_and_transition(self, bit: TransitionRequest, target_state:ControllerState):
		if self.controllerRequestTransitionField & bit:
			self.controllerState = target_state
			self._toggleRequestTransitionBit(bit, False)
			return True
		return False

	def jog(self, position:Position):
		commandToSend = Command(CommandId.MOVE, self.jogVelocity, position, None)
		self.commands.append(commandToSend)
	
	def setJogVelocity(self, velocity:float):
		self.jogVelocity = velocity

	def goHome(self):
		commandToSend = Command(CommandId.HOME, self.jogVelocity, None)
		self.commands.append(commandToSend)

	def activateManualMode(self):
		self._toggleRequestTransitionBit(TransitionRequest.TO_MANUAL,True)

	def stop(self):
		self._toggleRequestTransitionBit(TransitionRequest.TO_PAUSE,True)

	def start(self, commands:list):
		self.commands.extend(commands)
		self._toggleRequestTransitionBit(TransitionRequest.TO_RUNNING,True)

	def getLatestMachineInfo(self):
		#probably require a mutex
		return self.latestMachineInfo
	
	def connectionToMachine(self,comPort:str):
		self.com.open(comPort)
		self.comThread = threading.Thread(target=self.heartBeat)
		self.comThread.start

	def disconnectionFromMachine(self):
		self.com.close()
		self.closeEvent.set()
		self.comThread.join()

	def heartBeat(self):
		while not self.closeEvent.is_set():
			commandToSend = Command(CommandId.EMPTY, 0, None, None)

			match self.controllerState:
				case ControllerState.IDLE:
					if self._check_and_transition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING):
						pass
					elif self._check_and_transition(TransitionRequest.TO_MANUAL, ControllerState.MANUAL):
						pass

				case ControllerState.RUNNING:
					if self.latestMachineInfo[0] == MachineState.READY:
						commandToSend = self._nextCommand()
						if commandToSend.commandId == CommandId.PLACE:
							self.storage.components[commandToSend.piece].quantity =- 1
							self.storage.components[commandToSend.piece].piece = commandToSend.piece #TODO: confirm that piece position is the right one
						if self.lastCommand.commandId == CommandId.HOME:
							self.controllerState = ControllerState.DONE
					if self._check_and_transition(TransitionRequest.TO_PAUSE, ControllerState.PAUSE):
						pass

				case ControllerState.MANUAL:
					if self.latestMachineInfo[0] == MachineState.READY:
						nextCommand = self._nextCommand()
						if nextCommand is not None:
							commandToSend = nextCommand
					if self._check_and_transition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING):
						pass
					elif self._check_and_transition(TransitionRequest.TO_IDLE, ControllerState.IDLE):
						pass

				case ControllerState.PAUSE:
					commandToSend = Command(CommandId.STOP, 0, None, None)
					if self._check_and_transition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING):
						pass
					elif self._check_and_transition(TransitionRequest.TO_IDLE, ControllerState.IDLE):
						pass

				case ControllerState.DONE:
					if self._check_and_transition(TransitionRequest.TO_IDLE, ControllerState.IDLE):
						pass

			self._sendCommand(commandToSend)
			self._updateMachineInfo()
			self.closeEvent.wait(timeout=0.05)



	