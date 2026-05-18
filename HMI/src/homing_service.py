"""Homing workflow for the controller.

This service launches the homing command and waits until the machine reports
that it is ready again before calling the provided completion callback.
"""

import threading
import time

from command_interface import HomeCommand
from data import MachineState


class HomingService:
    """Drive the homing sequence in a background thread."""

    def __init__(self, controller):
        self._controller = controller

    def start(self, endingFunction = None):
        """Start homing if the controller is connected and not blocked."""
        if self._controller.blocked:
            return
        if not self._controller.isConnected():
            return
        homeThread = threading.Thread(target=self._homingThreadLoop, args=(endingFunction,))
        homeThread.start()

    def _homingThreadLoop(self, endingFunction = None):
        """Queue the home command and wait for the machine to become ready again."""
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