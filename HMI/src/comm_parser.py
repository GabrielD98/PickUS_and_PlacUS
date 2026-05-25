import struct
from typing import List

from command_interface import FirmwareCommandId
from data import MachineState, MAX_TOOLHEAD, get_status_packet_format


class CommParser:
    """Parse and log serial frames for debugging.

    The parser can be toggled on/off to avoid console noise.
    """

    def __init__(self, enabled: bool = False):
        self._enabled = enabled

    def setEnabled(self, enabled: bool):
        self._enabled = enabled

    def isEnabled(self) -> bool:
        return self._enabled

    def logOutgoing(self, frame: bytes):
        if not self._enabled:
            return
        info = self._parseCommandFrame(frame)
        print(f"[COMM PARSE OUT] {info}")

    def logIncoming(self, payload: bytes):
        if not self._enabled:
            return
        info = self._parseStatusFrame(payload)
        print(f"[COMM PARSE IN] {info}")

    def _parseCommandFrame(self, frame: bytes) -> str:
        if len(frame) < 7:
            return f"frame too small len={len(frame)}"

        command_id, command_number, payload_size = struct.unpack('<BIH', frame[:7])
        payload = frame[7:]
        command_name = self._commandName(command_id)

        if len(payload) != payload_size:
            return (
                f"cmd={command_name} num={command_number} payloadSize={payload_size} "
                f"actual={len(payload)}"
            )

        if command_id == int(FirmwareCommandId.STOP):
            return f"cmd=STOP num={command_number}"
        if command_id == int(FirmwareCommandId.PAUSE):
            return f"cmd=PAUSE num={command_number}"
        if command_id == int(FirmwareCommandId.MOVE):
            fmt = '<llllhhhh'
            if payload_size != struct.calcsize(fmt):
                return f"cmd=MOVE num={command_number} payloadSize={payload_size}"
            x, y, z, yaw, vx, vy, vz, vyaw = struct.unpack(fmt, payload)
            return (
                f"cmd=MOVE num={command_number} pos=({x},{y},{z},{yaw}) "
                f"vel=({vx},{vy},{vz},{vyaw})"
            )
        if command_id == int(FirmwareCommandId.HOME):
            fmt = '<hhhh'
            if payload_size != struct.calcsize(fmt):
                return f"cmd=HOME num={command_number} payloadSize={payload_size}"
            vx, vy, vz, vyaw = struct.unpack(fmt, payload)
            return f"cmd=HOME num={command_number} vel=({vx},{vy},{vz},{vyaw})"
        if command_id in (int(FirmwareCommandId.PICK), int(FirmwareCommandId.PLACE)):
            fmt = '<BxH'
            if payload_size != struct.calcsize(fmt):
                return f"cmd={command_name} num={command_number} payloadSize={payload_size}"
            toolhead, threshold = struct.unpack(fmt, payload)
            return f"cmd={command_name} num={command_number} toolhead={toolhead} threshold={threshold}"

        return f"cmd={command_name} num={command_number} payloadSize={payload_size}"

    def _parseStatusFrame(self, payload: bytes) -> str:
        fmt = get_status_packet_format()
        expected_size = struct.calcsize(fmt)
        if len(payload) < expected_size:
            return f"status too small len={len(payload)} expected={expected_size}"

        unpacked = struct.unpack(fmt, payload[:expected_size])
        machine_state = self._machineStateName(unpacked[0])
        command_name = self._commandName(unpacked[1])
        x, y, z, yaw = unpacked[2:6]

        pressures = list(unpacked[6:6 + MAX_TOOLHEAD])
        valve_start = 6 + MAX_TOOLHEAD
        valve_end = valve_start + MAX_TOOLHEAD
        valves = list(unpacked[valve_start:valve_end])
        pump_state = unpacked[-1]

        pressures_str = self._formatFloatList(pressures)
        valves_str = self._formatBoolList(valves)
        return (
            f"state={machine_state} cmd={command_name} pos=({x},{y},{z},{yaw}) "
            f"pressure={pressures_str} valve={valves_str} pump={bool(pump_state)}"
        )

    def _commandName(self, command_id: int) -> str:
        try:
            return FirmwareCommandId(command_id).name
        except ValueError:
            return f"UNKNOWN({command_id})"

    def _machineStateName(self, state_id: int) -> str:
        try:
            return MachineState(state_id).name
        except ValueError:
            return f"UNKNOWN({state_id})"

    def _formatFloatList(self, values: List[float]) -> str:
        return '[' + ', '.join(f"{value:.2f}" for value in values) + ']'

    def _formatBoolList(self, values: List[bool]) -> str:
        return '[' + ', '.join('1' if value else '0' for value in values) + ']'
