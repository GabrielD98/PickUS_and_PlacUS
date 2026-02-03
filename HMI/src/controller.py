import struct
import threading

from storage import Storage
from communication import Communication
from data import Position, Command, CommandId, ControllerState, MachineState, TransitionRequest




class Controller:
	"""
	Class that handles the command logic (what and when to send to the PNP).

	Attributes (all private except mutex):
	
		_storage (Storage):
			The storage of all the components to be placed
		_com (Communication):
			Serial communication interface
		_commands (list[Command]):
			List of commands that are ready to be sent
		_lastCommand (Command):
			Last command sent to the PNP
		_controllerState (ControllerState):
			Current controller state
		_latestMachineInfo (tuple[MachineState, Position]):
			Last information received from the PNP
		_closeEvent (threading.Event):
			Thread event used to close the communication thread
		_comThread (threading.Thread):
			Communication thread that runs the _controlLoop
		_controllerRequestTransitionField (int):
			Bit field of all current requested transitions
		mutex (threading.Lock):
			Used to ensure thread safety for all shared state
	"""
	
	def __init__(self):
		self._storage = Storage() # mutex on Storage?
		self._com = Communication()
		self._commands = []
		self._lastCommand = Command(CommandId.EMPTY,0, None, None)
		self._controllerState = ControllerState.IDLE
		self._latestMachineInfo = (MachineState.DISCONNECTED, Position(0,0,0,0))
		self._closeEvent = threading.Event()
		self._comThread = None
		self._controllerRequestTransitionField = 0
		self.mutex = threading.Lock()




	def queueCommand(self, command: Command):
		"""
		Add a single command to the execution queue.

		Parameters:
			command (Command):
				Command to add at the end of the queue.
		"""
		with self.mutex:
			self._commands.append(command)
	



	def queueCommands(self, commands: list[Command]):
		"""
		Add multiple commands to the execution queue.

		Parameters:
			commands (list[Command]):
				Commands to add at the end of the queue.
		"""
		with self.mutex:
			self._commands.extend(commands)




	def requestTransition(self, transition: TransitionRequest):
		"""
		Request a state machine transition.

		Parameters:
			transition (TransitionRequest):
				Transition request to apply to the state machine.
		"""
		with self.mutex:
			self._toggleRequestTransitionBit(transition, True)




	def getState(self) -> tuple[ControllerState, MachineState, Position]:
		"""
		Get current controller state, machine state, and position.

		Returns:
			tuple[ControllerState, MachineState, Position]:
				ControllerState:
					Current controller state.
				MachineState:
					Last known machine state.
				Position:
					Last known position of the machine.
				
		"""
		with self.mutex:
			machineState, position = self._latestMachineInfo
			controllerState = self._controllerState
		return (controllerState, machineState, position)
	



	def _sendCommand(self, command:Command):
		"""
		Pack and send the given command on the serial port.

		Parameters:
			command (Command):
				Command to send.
		"""
		p = command.position

		if(p is None):
			p = Position(0,0,0,0)

		byteBuffer = struct.pack('<Bfffff',
						    command.commandId,
							command.velocity, 
							p.x, p.y, p.z, p.yaw)

		self._com.sendData(byteBuffer)
	



	def _updateMachineInfo(self):
		"""
		Receive a machine info packet and update `latestMachineInfo`.

		Expected packet format (little-endian):
		  uint8_t machine_state
		  float32 x, y, z, yaw
		"""
		bytesBuffer = self._com.receiveData()
		format = '<Bffff'
		size = struct.calcsize(format)

		machineState, x, y, z, yaw = struct.unpack(format, bytesBuffer[:size])
		with self.mutex:
			self._latestMachineInfo = (MachineState(machineState), Position(x, y, z, yaw))



	def _nextCommand(self) -> Command:
		"""
		Return the first element of the attribute _commands if it's not empty.
		Update the last command sent.

		Returns:
			Command:
				Next command to send, or None if queue is empty.
				
		"""
		nextCommand = None
		with self.mutex:
			if self._commands:
				nextCommand = self._commands.pop(0)
				self._lastCommand = nextCommand
		return nextCommand
	



	def _toggleRequestTransitionBit(self, bit: TransitionRequest, state: bool):
		"""
		Toggle the requested bit to a given state

		Parameters:
			bit (TransitionRequest):
				Bit to toggle.
			state (bool):
				Request state for the bit
		"""
		if state:
			self._controllerRequestTransitionField |= bit
		else:
			self._controllerRequestTransitionField &= ~bit
	



	def _check_and_transition(self, bit: TransitionRequest, target_state:ControllerState) -> bool:
		"""
		Verify that a transition is due

		Parameters:
			bit (TransitionRequest):
				Transition bit to validate
			target_state (ControllerState):
				Next controller state if the transition is requested
		
		Returns:
			bool:
				True if a transition happen
				False if no transition happen
		"""
		with self.mutex:
			transitionMade = False
			if self._controllerRequestTransitionField & bit:
				self._controllerState = target_state
				self._controllerRequestTransitionField &= ~bit
				transitionMade = True
		return transitionMade
	



	def _handle_idle_state(self) -> Command:
		"""
		Handle IDLE state - wait for transition requests.
		
		Checks for pending transitions to RUNNING or MANUAL states.
		No commands are executed in this state.
		
		Returns:
			Command:
				Command to send when in idle state (always EMPTY).
		"""
		self._check_and_transition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING)
		self._check_and_transition(TransitionRequest.TO_MANUAL, ControllerState.MANUAL)
		return Command(CommandId.EMPTY, 0, None, None)




	def _handle_running_state(self) -> Command:
		"""Handle RUNNING state - execute command queue automatically.
		
		Executes queued commands sequentially when the machine is in READY state.
		For PLACE commands, decrements the component quantity in storage.
		Transitions to DONE state after HOME command completes.
		Can transition to PAUSE state on request.
		
		Returns:
			Command:
				Next command from queue if machine is READY, otherwise EMPTY command.
		"""
		commandToSend = Command(CommandId.EMPTY, 0, None, None)
		
		with self.mutex:
			machineState = self._latestMachineInfo[0]
		
		if machineState == MachineState.READY:
			commandToSend = self._nextCommand()
			if commandToSend and commandToSend.commandId == CommandId.PLACE:
				self._storage.components[commandToSend.piece].quantity -= 1
				self._storage.components[commandToSend.piece].piece = commandToSend.piece #TODO: confirm that piece position is the right one
			
			with self.mutex:
				lastCommandId = self._lastCommand.commandId
			
			if lastCommandId == CommandId.HOME:
				with self.mutex:
					self._controllerState = ControllerState.DONE
		
		self._check_and_transition(TransitionRequest.TO_PAUSE, ControllerState.PAUSE)
		return commandToSend




	def _handle_manual_state(self) -> Command:
		"""Handle MANUAL state - execute commands manually.
		
		Executes commands one at a time when the machine is in READY state,
		requiring manual confirmation for each command.
		Can transition to RUNNING or IDLE state on request.
		
		Returns:
			Command:
				Next command from queue if machine is READY, otherwise EMPTY command.
		"""
		commandToSend = Command(CommandId.EMPTY, 0, None, None)
		
		with self.mutex:
			machineState = self._latestMachineInfo[0]
		
		if machineState == MachineState.READY:
			nextCommand = self._nextCommand()
			if nextCommand is not None:
				commandToSend = nextCommand
		
		self._check_and_transition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING)
		self._check_and_transition(TransitionRequest.TO_IDLE, ControllerState.IDLE)
		return commandToSend




	def _handle_pause_state(self) -> Command:
		"""Handle PAUSE state - send stop command.
		
		Continuously sends STOP commands to halt machine operation.
		Can transition to RUNNING or IDLE state on request.
		
		Returns:
			Command:
				STOP command to halt machine execution.
		"""
		self._check_and_transition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING)
		self._check_and_transition(TransitionRequest.TO_IDLE, ControllerState.IDLE)
		return Command(CommandId.STOP, 0, None, None)




	def _handle_done_state(self) -> Command:
		"""Handle DONE state - job completed.
		
		Indicates that all queued commands have been executed successfully.
		Can transition back to IDLE state on request.
		
		Returns:
			Command:
				EMPTY command (no action needed).
		"""
		self._check_and_transition(TransitionRequest.TO_IDLE, ControllerState.IDLE)
		return Command(CommandId.EMPTY, 0, None, None)
	


	
	def _controlLoop(self):
		"""Main control loop managing state machine and communication.
		
		Runs continuously until closeEvent is set. On each iteration:
		1. Determines current controller state
		2. Dispatches to appropriate state handler
		3. Sends resulting command to machine
		4. Updates machine state information
		5. Waits 50ms before next iteration
		
		This method runs in a separate thread and is the core of the
		controller's state machine execution.
		"""
		state_handlers = {
			ControllerState.IDLE: self._handle_idle_state,
			ControllerState.RUNNING: self._handle_running_state,
			ControllerState.MANUAL: self._handle_manual_state,
			ControllerState.PAUSE: self._handle_pause_state,
			ControllerState.DONE: self._handle_done_state,
		}
		
		while not self._closeEvent.is_set():
			with self.mutex:
				currentState = self._controllerState
			
			handler = state_handlers.get(currentState)
			commandToSend = handler() if handler else Command(CommandId.EMPTY, 0, None, None)
			
			self._sendCommand(commandToSend)
			self._updateMachineInfo()
			self._closeEvent.wait(timeout=0.05)



	