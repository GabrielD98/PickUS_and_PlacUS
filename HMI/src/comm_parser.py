import struct
from typing import Callable, List

from command_interface import FirmwareCommandId
from data import MachineState, MAX_TOOLHEAD, get_status_packet_format


class CommLogFilter:
    """Filter for log listeners."""

    def __init__(self, directions: set[str] | None = None, command_ids: set[int] | None = None):
        self.directions = set(directions) if directions is not None else None
        self.command_ids = set(command_ids) if command_ids is not None else None

    def matches(self, direction: str, command_id: int | None) -> bool:
        if self.directions is not None and direction not in self.directions:
            return False
        if self.command_ids is not None:
            if command_id is None:
                return False
            if command_id not in self.command_ids:
                return False
        return True

    @staticmethod
    def parse_command_ids(text: str) -> set[int] | None:
        """Parse comma-separated numeric ids, ignoring non-numeric tokens."""
        tokens = [token.strip() for token in text.split(",") if token.strip()]
        if not tokens:
            return None

        command_ids: set[int] = set()
        for token in tokens:
            if not token.isdigit():
                continue
            command_ids.add(int(token))

        return command_ids or None


class CommParser:
    """Parse and log serial frames for debugging.

    The parser can be toggled on/off to avoid console noise.
    """

    def __init__(self, enabled: bool = False):
        self._enabled = enabled
        self._listeners: List[dict[str, object]] = []

    def setEnabled(self, enabled: bool):
        self._enabled = enabled

    def isEnabled(self) -> bool:
        return self._enabled

    def addListener(self, listener: Callable[[str, str], None], log_filter: CommLogFilter | None = None):
        for entry in self._listeners:
            if entry.get("listener") is listener:
                return
        self._listeners.append({"listener": listener, "filter": log_filter})

    def updateListenerFilter(self, listener: Callable[[str, str], None], log_filter: CommLogFilter | None):
        for entry in self._listeners:
            if entry.get("listener") is listener:
                entry["filter"] = log_filter
                return

    def removeListener(self, listener: Callable[[str, str], None]):
        for entry in list(self._listeners):
            if entry.get("listener") is listener:
                self._listeners.remove(entry)
                break

    def logOutgoing(self, frame: bytes):
        if not self._enabled:
            return
        info, command_id = self._parseCommandFrame(frame)
        self._emit("OUT", info, command_id)

    def logIncoming(self, payload: bytes):
        if not self._enabled:
            return
        info, command_id = self._parseStatusFrame(payload)
        self._emit("IN", info, command_id)

    def _emit(self, direction: str, message: str, command_id: int | None):
        """Emit log entries to listeners that pass their filter."""
        for entry in list(self._listeners):
            log_filter = entry.get("filter")
            if not self._passesFilter(log_filter, direction, command_id):
                continue
            try:
                entry.get("listener")(direction, message)
            except Exception:
                continue

    def _parseCommandFrame(self, frame: bytes) -> tuple[str, int | None]:
        if len(frame) < 7:
            return f"frame too small len={len(frame)}", None

        command_id, command_number, payload_size = struct.unpack('<BIH', frame[:7])
        payload = frame[7:]
        command_name = self._commandName(command_id)

        if len(payload) != payload_size:
            return (
                f"cmd={command_name} num={command_number} payloadSize={payload_size} "
                f"actual={len(payload)}"
            ), command_id

        if command_id == int(FirmwareCommandId.STOP):
            return f"cmd=STOP num={command_number}", command_id
        if command_id == int(FirmwareCommandId.PAUSE):
            return f"cmd=PAUSE num={command_number}", command_id
        if command_id == int(FirmwareCommandId.MOVE):
            fmt = '<llllhhhh'
            if payload_size != struct.calcsize(fmt):
                return f"cmd=MOVE num={command_number} payloadSize={payload_size}", command_id
            x, y, z, yaw, vx, vy, vz, vyaw = struct.unpack(fmt, payload)
            return (
                f"cmd=MOVE num={command_number} pos=({x},{y},{z},{yaw}) "
                f"vel=({vx},{vy},{vz},{vyaw})"
            ), command_id
        if command_id == int(FirmwareCommandId.HOME):
            fmt = '<hhhh'
            if payload_size != struct.calcsize(fmt):
                return f"cmd=HOME num={command_number} payloadSize={payload_size}", command_id
            vx, vy, vz, vyaw = struct.unpack(fmt, payload)
            return f"cmd=HOME num={command_number} vel=({vx},{vy},{vz},{vyaw})", command_id
        if command_id in (int(FirmwareCommandId.PICK), int(FirmwareCommandId.PLACE)):
            fmt = '<BxH'
            if payload_size != struct.calcsize(fmt):
                return f"cmd={command_name} num={command_number} payloadSize={payload_size}", command_id
            toolhead, threshold = struct.unpack(fmt, payload)
            return f"cmd={command_name} num={command_number} toolhead={toolhead} threshold={threshold}", command_id
        if command_id == int(FirmwareCommandId.SET_VALVE):
            fmt = '<BB'
            if payload_size != struct.calcsize(fmt):
                return f"cmd={command_name} num={command_number} payloadSize={payload_size}", command_id
            toolhead, enabled = struct.unpack(fmt, payload)
            return f"cmd={command_name} num={command_number} toolhead={toolhead} state={'ON' if enabled else 'OFF'}", command_id
        if command_id == int(FirmwareCommandId.SET_PUMP):
            fmt = '<B'
            if payload_size != struct.calcsize(fmt):
                return f"cmd={command_name} num={command_number} payloadSize={payload_size}", command_id
            enabled = struct.unpack(fmt, payload)[0]
            return f"cmd={command_name} num={command_number} state={'ON' if enabled else 'OFF'}", command_id

        return f"cmd={command_name} num={command_number} payloadSize={payload_size}", command_id

    def _parseStatusFrame(self, payload: bytes) -> tuple[str, int | None]:
        fmt = get_status_packet_format()
        expected_size = struct.calcsize(fmt)
        if len(payload) < expected_size:
            return f"status too small len={len(payload)} expected={expected_size}", None

        unpacked = struct.unpack(fmt, payload[:expected_size])
        machine_state = self._machineStateName(unpacked[0])
        command_name = self._commandName(unpacked[1])
        command_id = unpacked[1]
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
        ), command_id

    @staticmethod
    def _passesFilter(log_filter: CommLogFilter | None, direction: str, command_id: int | None) -> bool:
        if log_filter is None:
            return True
        return log_filter.matches(direction, command_id)

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
