import struct
import threading
import time

from command_interface import CommandPacket, CommandInterface, HomeCommand, PauseCommand, PlaceCommand
from communication import Communication
from data import ControllerState, MachineState, Position, TransitionRequest, get_status_packet_format
from geometry import StepPosition, stepToCoord


RESPONSE_TIMOUT = 200 #ms
MAX_MISSED_RESPONSES = 3


class CommandDispatcher:
    def __init__(self, controller):
        self._controller = controller

    def queueCommand(self, command: CommandPacket):
        with self._controller.mutex:
            self._controller._commands.append(command)

    def queueCommands(self, commands: list[CommandPacket]):
        with self._controller.mutex:
            self._controller._commands.extend(commands)

    def clearCommands(self):
        with self._controller.mutex:
            self._controller._commands = []

    def nextCommand(self) -> CommandPacket | None:
        nextCommand = None
        with self._controller.mutex:
            if self._controller._commands:
                nextCommand = self._controller._commands.pop(0)
                self._controller._lastCommand = nextCommand
        return nextCommand

    def requeueLastCommand(self):
        with self._controller.mutex:
            if self._controller._lastCommand is not None:
                self._controller._commands.insert(0, self._controller._lastCommand)

    def sendCommand(self, command: CommandPacket | None):
        if self._controller._com is None:
            return

        if command is None:
            heartbeat = PauseCommand()
            packet = self._controller._commandInterface.buildPacket(heartbeat, True)
            if packet is not None:
                self._controller._com.sendData(packet)
                self._controller._lastSentCommand = heartbeat
            return

        is_new_command = command is not self._controller._lastSentCommand
        packet = self._controller._commandInterface.buildPacket(command, is_new_command)

        if packet is not None:
            self._controller._com.sendData(packet)
            self._controller._lastSentCommand = command


class PnPStateMachine:
    def __init__(self, controller, dispatcher: CommandDispatcher):
        self._controller = controller
        self._dispatcher = dispatcher

    def requestTransition(self, transition: TransitionRequest):
        with self._controller.mutex:
            self._toggleRequestTransitionBit(transition, True)

    def _toggleRequestTransitionBit(self, bit: TransitionRequest, state: bool):
        if state:
            self._controller._controllerRequestTransitionField |= bit.value
        else:
            self._controller._controllerRequestTransitionField &= ~bit.value

    def _checkAndTransition(self, bit: TransitionRequest, target_state: ControllerState) -> bool:
        with self._controller.mutex:
            transitionMade = False
            if self._controller._controllerRequestTransitionField & bit.value:
                self._controller._controllerState = target_state
                self._controller._controllerRequestTransitionField &= ~bit.value
                transitionMade = True
        return transitionMade

    def handleIdleState(self) -> CommandPacket | None:
        self._checkAndTransition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING)
        self._checkAndTransition(TransitionRequest.TO_MANUAL, ControllerState.MANUAL)
        return None

    def handleRunningState(self) -> CommandPacket | None:
        commandToSend = None

        with self._controller.mutex:
            machineState = self._controller._latestMachineInfo[0]

        if machineState == MachineState.READY:
            nextCommand = self._dispatcher.nextCommand()
            if nextCommand is not None:
                commandToSend = nextCommand
            if isinstance(commandToSend, PlaceCommand):
                if commandToSend.piece is not None and commandToSend.piece in self._controller._storage.components:
                    self._controller._storage.components[commandToSend.piece].quantity -= 1
                    self._controller._storage.components[commandToSend.piece].piece = commandToSend.piece

            with self._controller.mutex:
                lastCommand = self._controller._lastCommand

            if isinstance(lastCommand, HomeCommand):
                with self._controller.mutex:
                    self._controller._controllerState = ControllerState.DONE
        elif self._controller._lastCommand is not None:
            commandToSend = self._controller._lastCommand

        self._checkAndTransition(TransitionRequest.TO_PAUSE, ControllerState.PAUSE)
        return commandToSend

    def handleManualState(self) -> CommandPacket | None:
        commandToSend = None

        with self._controller.mutex:
            machineState = self._controller._latestMachineInfo[0]

        if machineState == MachineState.READY:
            nextCommand = self._dispatcher.nextCommand()
            if nextCommand is not None:
                commandToSend = nextCommand
        elif self._controller._lastCommand is not None:
            commandToSend = self._controller._lastCommand

        self._checkAndTransition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING)
        self._checkAndTransition(TransitionRequest.TO_IDLE, ControllerState.IDLE)
        return commandToSend

    def handlePauseState(self) -> CommandPacket | None:
        if self._checkAndTransition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING):
            self._dispatcher.requeueLastCommand()
            return None

        if self._checkAndTransition(TransitionRequest.TO_IDLE, ControllerState.IDLE):
            self._dispatcher.clearCommands()
            return None

        return PauseCommand()

    def handleDoneState(self) -> CommandPacket | None:
        self._checkAndTransition(TransitionRequest.TO_IDLE, ControllerState.IDLE)
        return None

    def nextCommand(self) -> CommandPacket | None:
        with self._controller.mutex:
            currentState = self._controller._controllerState

        stateHandlers = {
            ControllerState.IDLE: self.handleIdleState,
            ControllerState.RUNNING: self.handleRunningState,
            ControllerState.MANUAL: self.handleManualState,
            ControllerState.PAUSE: self.handlePauseState,
            ControllerState.DONE: self.handleDoneState,
        }
        handler = stateHandlers.get(currentState)
        return handler() if handler else None


class MachineTelemetryDecoder:
    def __init__(self, controller):
        self._controller = controller

    def updateMachineInfo(self):
        if self._controller._com is None:
            return

        format = get_status_packet_format()
        size = struct.calcsize(format)
        bytesBuffer = self._controller._com.receiveData(size)

        if bytesBuffer is None or len(bytesBuffer) < size:
            if (time.time() * 1000) - self._controller._timeSinceLastResponse > RESPONSE_TIMOUT:
                self._controller._missedResponses += 1
                if self._controller._missedResponses >= MAX_MISSED_RESPONSES:
                    self._controller._connected = False
            return

        try:
            machineState, currentCommandId, x, y, z, yaw, pressure, valveState, pumpState = struct.unpack(format, bytesBuffer[:size])
            position = stepToCoord(StepPosition(x, y, z, yaw))
            with self._controller.mutex:
                self._controller._latestMachineInfo = (MachineState(machineState), position)
                self._controller._latestCommandId = currentCommandId
        except (struct.error, ValueError):
            if self._controller._com.isPortOpen():
                self._controller._com.ser.reset_input_buffer()
            return

        self._controller._connected = True
        self._controller._missedResponses = 0
        self._controller._timeSinceLastResponse = time.time() * 1000


class HomingService:
    def __init__(self, controller):
        self._controller = controller

    def start(self, endingFunction = None):
        if self._controller.blocked:
            return
        if not self._controller.isConnected():
            return
        homeThread = threading.Thread(target=self._homingThreadLoop, args=(endingFunction,))
        homeThread.start()

    def _homingThreadLoop(self, endingFunction = None):
        self._controller.blocked = True
        homeCommand = HomeCommand()
        self._controller.queueCommand(homeCommand)

        time.sleep(0.5)
        while not self._controller.getMachineState() == MachineState.READY:
            if not self._controller.isConnected():
                break
            time.sleep(0.5)

        if endingFunction is not None:
            endingFunction()
        self._controller.homed = True
        self._controller.blocked = False