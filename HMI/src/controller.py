import struct
import threading

from storage import Storage
from communication import Communication
from data import Position, Command, CommandId, ControllerState, MachineState, TransitionRequest
import time
from typing import List

RESPONSE_TIMOUT = 200 #ms




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
	
	#TODO continue when pause


	def __init__(self):

		if hasattr(self, 'initialized'):
			return
		self.initialized = True

		
		self._storage = Storage() #TODO mutex on Storage?
		self._com = None
		self.commandInWaiting:List[Command] = []
		self._commands = []
		self._lastCommand = Command(CommandId.EMPTY,0, None, None)
		self._controllerState = ControllerState.IDLE
		self._latestMachineInfo = (MachineState.HOMING, Position(0,0,0,0))
		self._closeEvent = threading.Event()
		self._comThread = None
		self._controllerRequestTransitionField = 0
		self._time_since_last_response:float = -1
		self._connected = False
		self.mutex = threading.Lock()

		self.homed = False
		self.blocked = False



	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Controller, cls).__new__(cls)
		return cls.instance


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
		Legacy TODO remove
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
	



	def connectionToMachine(self,comPort:str, baudrate:int):
		"""
		Open the serial port and start the controlLoop thread

		Parameters:
			comPort (str):
				serial port to opne	
			baudrate (int):
				port speed
		"""

		self._time_since_last_response = time.time() * 1000
		self._com = Communication(comPort, baudrate)
		self._com.open()
		self._closeEvent = threading.Event()
		self._comThread = threading.Thread(target=self._controlLoop)
		self._comThread.start()




	def disconnectionFromMachine(self):
		"""
		Close the serial port and stop the controlLoop thread
				
		"""
		if self._com is not None:
			self._com.close()
			self._com = None
		
		if self._comThread is not None:
			self._closeEvent.set()
			self._comThread.join()
			self._comThread = None

		self._connected = False




	def isConnected(self):
		return self._connected




	def isPortOpen(self):
		return self._comThread is not None




	def start_pnp(self):
		"""
		Begins the PnP procedures
		Queues the commands in wating and transition the state to running
		"""
		if self.blocked:
			return
		self.requestTransition(TransitionRequest.TO_RUNNING)
		self.queueCommands(self.commandInWaiting)
		#print(self.commandInWaiting)
		print("STARTING THE SLICE")





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
						    command.commandId.value,
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
		format = '<Bffff'
		size = struct.calcsize(format)
		bytesBuffer = self._com.receiveData(size)

		if bytesBuffer is None or len(bytesBuffer) < size:
			if (time.time()*1000) - self._time_since_last_response > RESPONSE_TIMOUT:
				self._connected = False
			return
		try:
			machineState, x, y, z, yaw = struct.unpack(format, bytesBuffer[:size])
			#print("reception : ", machineState, x, y, z, yaw)
			with self.mutex:
				self._latestMachineInfo = (MachineState(machineState), Position(x, y, z, yaw))
				
		except (struct.error, ValueError):
			# Discard invalid/garbage data and resync
			if self._com.isPortOpen():
				self._com.ser.reset_input_buffer()
			return
		
		self._connected =  True
		self._time_since_last_response = time.time() * 1000




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
			self._controllerRequestTransitionField |= bit.value
		else:
			self._controllerRequestTransitionField &= ~bit.value
	



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
			if self._controllerRequestTransitionField & bit.value:
				self._controllerState = target_state
				self._controllerRequestTransitionField &= ~bit.value
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
			nextCommand = self._nextCommand()
			if nextCommand is not None:
				commandToSend = nextCommand
			if commandToSend.commandId == CommandId.PLACE:
				if commandToSend.piece is not None and commandToSend.piece in self._storage.components:
					self._storage.components[commandToSend.piece].quantity -= 1
					self._storage.components[commandToSend.piece].piece = commandToSend.piece
			
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

		if self._check_and_transition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING):
			self._commands.insert(0, self._lastCommand)
			
		if self._check_and_transition(TransitionRequest.TO_IDLE, ControllerState.IDLE):
			self._commands = [] 

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
			#print(commandToSend)
			
			self._sendCommand(commandToSend)
			self._updateMachineInfo()

			#TODO no magic number, and calc the time taken to do previous operations maybe?
			self._closeEvent.wait(timeout=0.05)





	def homing_thread(self, ending_function = None):
		"""
		Thread that homes the PnP. The thread will end 
		when the PnP is Homed or if the process is interupted

		Parameters:
			ending_function : a function to be called when the homing is done
								#TODO add signal
		"""
		self.blocked = True
		home_cmd = Command(CommandId.HOME,
			velocity=0,
			position=None,
			piece=None)
		self.queueCommand(home_cmd)

		time.sleep(0.5)
		while not self.get_machine_state() == MachineState.READY:
			if not self.isConnected():
				break
			time.sleep(0.5)

		if ending_function is not None:
			ending_function()
		self.homed = True
		self.blocked = False





	def go_home(self, ending_function):
		"""
		Starts the homing thread 

		Parameters:
			ending_function : a function to be called when the homing is done
								#TODO add signal
		"""
		if self.blocked :
			return
		if not self.isConnected():
			return
		home_thread = threading.Thread(target=self.homing_thread,  args=(ending_function,))
		home_thread.start()




	def get_machine_state(self) -> MachineState:
		"""return the state of the Machine (the ESP32)"""
		with self.mutex:
			state = self._latestMachineInfo[0]
		return state




	def get_gripper_position(self) -> Position:
		"""return the Position of the tip of the gripper (x, y, z, yaw)"""
		with self.mutex:
			position = self._latestMachineInfo[1]
		return position




	def get_controller_state(self) -> ControllerState:
		"""return the state of the Machine (this controller)"""
		return  self._controllerState




	def set_pnp_commands(self, command:Command):
		"""sets the list of commands for the slice without starting the PnP
		Parameters:
			command (Command):
				Command to add at the end of the queue.
		"""
		if self.blocked:
			return
		self.commandInWaiting = command 






	def pause_pnp(self):
		"""
		Pauses the PnP. Interupts the current action 
		and waits for either a Continue command or a Stop command
		"""
		self.requestTransition(TransitionRequest.TO_PAUSE)




	def transition_to_running(self):
		"""Changes the machine state to RUNNING (slicing is occuring)"""
		self.requestTransition(TransitionRequest.TO_RUNNING)




	def transition_to_manual(self):
		"""Change the machine state to MANNUAL (jogging is occuring)"""
		self.requestTransition(TransitionRequest.TO_MANUAL)




	def transition_to_idle(self):
		"""Change the machine state to IDLE (waiting for commands)"""
		self.requestTransition(TransitionRequest.TO_IDLE)




	def continue_pnp(self):
		"""Continues the interrupted command by the Pause action"""
		self.requestTransition(TransitionRequest.TO_RUNNING)

