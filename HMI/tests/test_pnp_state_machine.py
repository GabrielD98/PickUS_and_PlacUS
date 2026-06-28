import os
import sys
import threading
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from command_dispatcher import CommandDispatcher, CommandPacket
from command_interface import HomeCommand
from data import ControllerState, MachineState, Position
from pnp_state_machine import PnPStateMachine


class _FakeStorage:
    def __init__(self):
        self.components = {}


class _FakeController:
    def __init__(self):
        self.mutex = threading.Lock()
        self._commands = []
        self._lastCommand = None
        self._controllerState = ControllerState.RUNNING
        self._latestMachineState = MachineState.READY
        self._latestMachinePosition = Position(0, 0, 0, 0)
        self._controllerRequestTransitionField = 0
        self._storage = _FakeStorage()

    def getMachineState(self) -> MachineState:
        return self._latestMachineState
    
    def getLastCommand(self) -> CommandPacket:
        return self._lastCommand

class TestPnPStateMachine(unittest.TestCase):
    def test_home_does_not_set_done_before_completion(self):
        controller = _FakeController()
        dispatcher = CommandDispatcher(controller)
        state_machine = PnPStateMachine(controller, dispatcher)

        home = HomeCommand()
        controller._commands = [home]

        # First READY cycle should dequeue and send HOME, but remain RUNNING.
        first_command = state_machine.handleRunningState()
        controller._lastCommand = first_command
        self.assertIs(first_command, home)
        self.assertEqual(controller._controllerState, ControllerState.RUNNING)

        # While machine is still not READY, controller must keep resending HOME and stay RUNNING.
        controller._latestMachineState = MachineState.RUNNING
        second_command = state_machine.handleRunningState()
        self.assertIs(second_command, home)
        self.assertEqual(controller._controllerState, ControllerState.RUNNING)

        # Only after machine reports READY again with empty queue should state transition to DONE.
        controller._latestMachineState = MachineState.READY
        third_command = state_machine.handleRunningState()
        print(third_command)
        self.assertIsNone(third_command)
        self.assertEqual(controller._controllerState, ControllerState.DONE)


if __name__ == '__main__':
    unittest.main()
