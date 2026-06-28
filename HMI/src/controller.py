import threading
import time
from typing import List

from command_interface import CommandInterface, CommandPacket, PauseCommand, StopCommand
from comm_parser import CommLogFilter, CommParser
from communication import Communication
from command_dispatcher import CommandDispatcher
from homing_service import HomingService
from machine_telemetry_decoder import MachineTelemetryDecoder
from pnp_state_machine import PnPStateMachine
from data import ControllerState, MachineState, Position, TransitionRequest, MAX_TOOLHEAD
from storage import Storage


class Controller:
    """Facade over command queueing, state transitions, telemetry, and homing."""

    def __init__(self):
        if hasattr(self, "initialized"):
            return
        self.initialized = True

        self._storage = Storage()
        self._com = None
        self.commandInWaiting: List[CommandPacket] = []
        self._commands = []
        self._lastCommand: CommandPacket | None = None
        self._controllerState = ControllerState.IDLE
        self._latestCommandId = 0
        self._latestCommandNumber = 0
        self._latestMachineState = MachineState.READY
        self._latestMachinePosition = Position(0, 0, 0, 0)
        self._latestMachinePressure: float = 0.0
        self._latestMachinePressures: list[float] = [0.0 for _ in range(MAX_TOOLHEAD)]
        self._latestMachineValveStates: list[bool] = [False for _ in range(MAX_TOOLHEAD)]
        self._latestMachinePumpState: bool = False
        self._commandInterface = CommandInterface()
        self._commParser = CommParser()
        self._closeEvent = threading.Event()
        self._comThread = None
        self._controllerRequestTransitionField = 0
        self._timeSinceLastResponse: float = -1
        self._missedResponses = 0
        self._connected = False
        self._stopRequested = False
        self._commandParsingEnabled = True
        self.mutex = threading.Lock()

        self._commandDispatcher = CommandDispatcher(self)
        self._stateMachine = PnPStateMachine(self, self._commandDispatcher)
        self._telemetryDecoder = MachineTelemetryDecoder(self)
        self._homingService = HomingService(self)

        self.homed = False
        self.blocked = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Controller, cls).__new__(cls)
        return cls.instance

    def queueCommand(self, command: CommandPacket):
        with self.mutex:
            self._commands.append(command)

    def queueCommands(self, commands: list[CommandPacket]):
        with self.mutex:
            self._commands.extend(commands)

    def requestTransition(self, transition: TransitionRequest):
        self._stateMachine.requestTransition(transition)

    def connectionToMachine(self, comPort: str, baudrate: int):
        self._timeSinceLastResponse = time.time() * 1000
        self._com = Communication(comPort, baudrate, self._commParser)
        self._com.open()
        self._commParser.setEnabled(self._commandParsingEnabled)
        self._closeEvent = threading.Event()
        self._comThread = threading.Thread(target=self._controlLoop)
        self._comThread.start()

    def disconnectionFromMachine(self):
        if self._com is not None:
            self._com.close()
            self._com = None

        if self._comThread is not None:
            self._closeEvent.set()
            self._comThread.join()
            self._comThread = None

        self._connected = False

    def isConnected(self) -> bool:
        return self._connected

    def isPortOpen(self):
        return self._comThread is not None

    def setCommandParsingEnabled(self, enabled: bool):
        self._commandParsingEnabled = enabled
        self._commParser.setEnabled(enabled)

    def isCommandParsingEnabled(self) -> bool:
        return self._commandParsingEnabled

    def addCommLogListener(self, listener):
        self._commParser.addListener(listener)

    def updateCommLogListenerFilter(self, listener, log_filter: CommLogFilter | None):
        self._commParser.updateListenerFilter(listener, log_filter)

    def removeCommLogListener(self, listener):
        self._commParser.removeListener(listener)

    def start_pnp(self):
        if self.blocked:
            return
        self._stateMachine.requestTransition(TransitionRequest.TO_RUNNING)
        self._commandDispatcher.queueCommands(self.commandInWaiting)

    def goHome(self, endingFunction):
        if self.blocked:
            return
        if not self.isConnected():
            return
        self._homingService.start(endingFunction)

    def getMachineState(self) -> MachineState:
        with self.mutex:
            state = self._latestMachineState
        return state
    
    def getMachineCommandNumber(self) -> int:
        with self.mutex:
            commandNumber = self._latestCommandNumber
        return commandNumber
    
    def getGripperPosition(self) -> Position:
        with self.mutex:
            position = self._latestMachinePosition
        return position
    
    def getMachinePressure(self) -> float:
        with self.mutex:
            pressure = self._latestMachinePressure
        return pressure

    def getMachinePressures(self) -> list[float]:
        with self.mutex:
            pressures = list(self._latestMachinePressures)
        return pressures

    def getMachineValveStates(self) -> list[bool]:
        with self.mutex:
            valves = list(self._latestMachineValveStates)
        return valves

    def getMachinePumpState(self) -> bool:
        with self.mutex:
            pump = self._latestMachinePumpState
        return pump

    def getLatestCommandId(self) -> int:
        with self.mutex:
            commandId = self._latestCommandId
        return commandId

    def getControllerState(self) -> ControllerState:
        with self.mutex:
            controllerState = self._controllerState
        return controllerState
    
    def getLastCommand(self) -> CommandPacket:
        with self.mutex:
            lastCommand = self._lastCommand
        return lastCommand

    def setPnpCommands(self, commands: list[CommandPacket]):
        if self.blocked:
            return
        self.commandInWaiting = commands

    def pausePnP(self):
        self.requestTransition(TransitionRequest.TO_PAUSE)

    def toggleRunningMode(self):
        self.requestTransition(TransitionRequest.TO_RUNNING)

    def toggleManualMode(self):
        self.requestTransition(TransitionRequest.TO_MANUAL)

    def toggleIDLEMode(self):
        self._commandDispatcher.clearCommands()
        self.requestTransition(TransitionRequest.TO_IDLE)

    def stopPnP(self):
        if self.blocked:
            return
        self._commandDispatcher.clearCommands()
        self._commandDispatcher.sendCommand(StopCommand())
        self.requestTransition(TransitionRequest.TO_IDLE)

    def continuePnP(self):
        self.requestTransition(TransitionRequest.TO_RUNNING)

    def _controlLoop(self):
        while not self._closeEvent.is_set():
            if self._telemetryDecoder.updateMachineInfo():
                commandToSend = self._stateMachine.nextCommand()
                self._commandDispatcher.sendCommand(commandToSend)
            self._closeEvent.wait(timeout=0.01)