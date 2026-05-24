"""Decode telemetry packets received from the machine.

This service updates the controller with the latest machine state and gripper
position by unpacking the binary status frame sent by the ESP32 firmware.
"""

import struct
import time

from data import MachineState, Position, get_status_packet_format
from geometry import StepPosition, stepToCoord


RESPONSE_TIMOUT = 200 #ms
MAX_MISSED_RESPONSES = 3


class MachineTelemetryDecoder:
    """Decode the latest telemetry frame and update controller state."""

    def __init__(self, controller):
        self._controller = controller

    def updateMachineInfo(self):
        """Refresh the controller with the latest packet from the machine."""
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
                self._controller._latestMachinePressure = pressure
        except (struct.error, ValueError):
            if self._controller._com.isPortOpen():
                self._controller._com.ser.reset_input_buffer()
            return

        self._controller._connected = True
        self._controller._missedResponses = 0
        self._controller._timeSinceLastResponse = time.time() * 1000