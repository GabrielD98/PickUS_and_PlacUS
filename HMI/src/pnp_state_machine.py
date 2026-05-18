"""State machine for pick-and-place controller transitions.

This service decides which command should be sent next based on the current
controller state, machine readiness, and pending transition requests.
"""

from command_interface import CommandPacket, HomeCommand, PauseCommand, PlaceCommand
from data import ControllerState, MachineState, TransitionRequest


class PnPStateMachine:
    """Resolve controller state transitions and next commands to send."""

    def __init__(self, controller, dispatcher):
        self._controller = controller
        self._dispatcher = dispatcher

    def requestTransition(self, transition: TransitionRequest):
        """Request a controller state transition."""
        with self._controller.mutex:
            self._toggleRequestTransitionBit(transition, True)

    def _toggleRequestTransitionBit(self, bit: TransitionRequest, state: bool):
        """Set or clear a pending transition flag."""
        if state:
            self._controller._controllerRequestTransitionField |= bit.value
        else:
            self._controller._controllerRequestTransitionField &= ~bit.value

    def _checkAndTransition(self, bit: TransitionRequest, target_state: ControllerState) -> bool:
        """Apply a transition if the corresponding bit is set."""
        with self._controller.mutex:
            transitionMade = False
            if self._controller._controllerRequestTransitionField & bit.value:
                self._controller._controllerState = target_state
                self._controller._controllerRequestTransitionField &= ~bit.value
                transitionMade = True
        return transitionMade

    def handleIdleState(self) -> CommandPacket | None:
        """Resolve commands while the controller is idle."""
        self._checkAndTransition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING)
        self._checkAndTransition(TransitionRequest.TO_MANUAL, ControllerState.MANUAL)
        return None

    def handleRunningState(self) -> CommandPacket | None:
        """Resolve commands while the controller is running."""
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
        """Resolve commands while the controller is in manual mode."""
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
        """Resolve commands while the controller is paused."""
        if self._checkAndTransition(TransitionRequest.TO_RUNNING, ControllerState.RUNNING):
            self._dispatcher.requeueLastCommand()
            return None

        if self._checkAndTransition(TransitionRequest.TO_IDLE, ControllerState.IDLE):
            self._dispatcher.clearCommands()
            return None

        return PauseCommand()

    def handleDoneState(self) -> CommandPacket | None:
        """Resolve commands after a completed pick-and-place cycle."""
        self._checkAndTransition(TransitionRequest.TO_IDLE, ControllerState.IDLE)
        return None

    def nextCommand(self) -> CommandPacket | None:
        """Return the next command the controller should send."""
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