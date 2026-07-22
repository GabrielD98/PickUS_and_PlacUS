"""Decode telemetry packets received from the machine.

This service updates the controller with the latest machine state and gripper
position by unpacking the binary status frame sent by the ESP32 firmware.
"""

import struct
import time

from data import MachineState, Position, get_status_packet_format, MAX_TOOLHEAD
from geometry import StepPosition, stepToCoord

class MachineTelemetryDecoder:
    """Decode the latest telemetry frame and update controller state."""

    def __init__(self, controller):
        self._controller = controller

    def updateMachineInfo(self) -> bool:
        """Refresh the controller with the latest packet from the machine."""
        if self._controller._com is None:
            return False

        format = get_status_packet_format()
        size = struct.calcsize(format)
        bytesBuffer = self._controller._com.receiveData(size)

        if bytesBuffer is None or len(bytesBuffer) < size:
                return False

        try:
            lastMachineState = self._controller.getMachineState()
            unpacked = struct.unpack(format, bytesBuffer[:size])
            machineState = unpacked[0]
            currentCommandId = unpacked[1]
            currentCommandNumber = unpacked[2]
            x, y, z, yaw = unpacked[3:7]
            pressure_start = 7
            pressure_end = pressure_start + MAX_TOOLHEAD
            valve_start = pressure_end
            valve_end = valve_start + MAX_TOOLHEAD
            pressures = list(unpacked[pressure_start:pressure_end])
            valves = [bool(v) for v in unpacked[valve_start:valve_end]]
            pump_state = bool(unpacked[-1])

            position = stepToCoord(StepPosition(x, y, z, yaw))
            with self._controller.mutex:
                self._controller._latestMachineState = MachineState(machineState)
                self._controller._latestMachinePosition = position
                self._controller._latestCommandId = currentCommandId
                self._controller._latestCommandNumber = currentCommandNumber
                self._controller._latestMachinePressure = pressures[0] if pressures else 0.0
                self._controller._latestMachinePressures = pressures
                self._controller._latestMachineValveStates = valves
                self._controller._latestMachinePumpState = pump_state
        except (struct.error, ValueError):
            if self._controller._com.isPortOpen():
                self._controller._com.ser.reset_input_buffer()
            return

        self._controller._connected = True
        return True