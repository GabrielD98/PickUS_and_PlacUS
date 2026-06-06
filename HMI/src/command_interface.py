import struct
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Protocol, runtime_checkable

from data import MAX_TOOLHEAD, Piece, Position
from geometry import CartesianVelocity, coordToStep, velocityToStep


DEFAULT_TOOLHEAD_INDEX = 0
DEFAULT_PICK_PRESSURE_KPA = 75
DEFAULT_PLACE_PRESSURE_KPA = 0
# Backwards-compatible default (used where a single default existed previously)
DEFAULT_PRESSURE_THRESHOLD_KPA = DEFAULT_PLACE_PRESSURE_KPA
DEFAULT_HOME_VELOCITY = CartesianVelocity(-50.0, -50.0, 50.0, 50.0)


class FirmwareCommandId(IntEnum):
    STOP = 0
    PAUSE = 1
    MOVE = 2
    PICK = 3
    PLACE = 4
    HOME = 5
    SET_VALVE = 6
    SET_PUMP = 7


@dataclass(frozen=True)
class PacketDefaults:
    toolheadIndex: int = DEFAULT_TOOLHEAD_INDEX
    pressureThresholdKpa: int = DEFAULT_PRESSURE_THRESHOLD_KPA

    def resolveToolheadIndex(self, commandToolheadIndex: int | None) -> int:
        toolheadIndex = self.toolheadIndex if commandToolheadIndex is None else commandToolheadIndex
        if toolheadIndex >= MAX_TOOLHEAD:
            raise ValueError(f"toolhead_index must be < MAX_TOOLHEAD ({MAX_TOOLHEAD})")
        return toolheadIndex

    def resolvePressureThreshold(self, commandPressureThresholdKpa: int | None) -> int:
        return self.pressureThresholdKpa if commandPressureThresholdKpa is None else commandPressureThresholdKpa


@runtime_checkable
class SerializableCommand(Protocol):
    @property
    def commandId(self) -> FirmwareCommandId:
        ...

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        ...


@dataclass(frozen=True)
class StopCommand:
    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.STOP

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        return b""


@dataclass(frozen=True)
class PauseCommand:
    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.PAUSE

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        return b""


@dataclass(frozen=True)
class MoveCommand:
    position: Position
    velocity: CartesianVelocity

    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.MOVE

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        positionStep = coordToStep(self.position)
        velocityStep = velocityToStep(self.velocity)
        return struct.pack(
            '<llllhhhh',
            positionStep.x,
            positionStep.y,
            positionStep.z,
            positionStep.yaw,
            velocityStep.x,
            velocityStep.y,
            velocityStep.z,
            velocityStep.yaw,
        )


@dataclass(frozen=True)
class HomeCommand:
    velocity: CartesianVelocity = field(default_factory=lambda: DEFAULT_HOME_VELOCITY)

    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.HOME

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        velocityStep = velocityToStep(self.velocity)
        return struct.pack(
            '<hhhh',
            velocityStep.x,
            velocityStep.y,
            velocityStep.z,
            velocityStep.yaw,
        )


@dataclass(frozen=True)
class PickCommand:
    toolheadIndex: int | None = DEFAULT_TOOLHEAD_INDEX
    pressureThresholdKpa: int | None = DEFAULT_PICK_PRESSURE_KPA

    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.PICK

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        toolheadIndex = defaults.resolveToolheadIndex(self.toolheadIndex)
        pressureThresholdKpa = defaults.resolvePressureThreshold(self.pressureThresholdKpa)
        return struct.pack('<BxH', toolheadIndex, pressureThresholdKpa)


@dataclass(frozen=True)
class PlaceCommand:
    toolheadIndex: int | None = DEFAULT_TOOLHEAD_INDEX
    pressureThresholdKpa: int | None = DEFAULT_PLACE_PRESSURE_KPA
    piece: Piece | None = None

    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.PLACE

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        toolheadIndex = defaults.resolveToolheadIndex(self.toolheadIndex)
        pressureThresholdKpa = defaults.resolvePressureThreshold(self.pressureThresholdKpa)
        return struct.pack('<BxH', toolheadIndex, pressureThresholdKpa)


@dataclass(frozen=True)
class SetValveCommand:
    toolheadIndex: int | None = DEFAULT_TOOLHEAD_INDEX
    enabled: bool = False

    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.SET_VALVE

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        toolheadIndex = defaults.resolveToolheadIndex(self.toolheadIndex)
        return struct.pack('<BB', toolheadIndex, 1 if self.enabled else 0)


@dataclass(frozen=True)
class SetPumpCommand:
    enabled: bool = False

    @property
    def commandId(self) -> FirmwareCommandId:
        return FirmwareCommandId.SET_PUMP

    def toPayload(self, defaults: PacketDefaults) -> bytes:
        return struct.pack('<B', 1 if self.enabled else 0)


CommandPacket = (
    StopCommand
    | PauseCommand
    | MoveCommand
    | HomeCommand
    | PickCommand
    | PlaceCommand
    | SetValveCommand
    | SetPumpCommand
)


class CommandInterface:
    """Build ESP32 command packets from explicit HMI command types."""

    def __init__(self, toolheadIndex: int = DEFAULT_TOOLHEAD_INDEX, pressureThresholdKpa: int = DEFAULT_PRESSURE_THRESHOLD_KPA):
        self._defaults = PacketDefaults(toolheadIndex=toolheadIndex, pressureThresholdKpa=pressureThresholdKpa)
        self._commandNumber = 0

    def buildPacket(self, command: CommandPacket | None, isNewCommand: bool = True) -> bytes | None:
        """Build the inner firmware command frame payload.
        
        Args:
            command: The command packet to build.
            isNewCommand: If True, increment command number. If False, reuse current number (for resends).
        """
        if command is None:
            return None

        serializableCommand = command
        if not isinstance(serializableCommand, SerializableCommand):
            raise TypeError(f"Unsupported command type: {type(command)!r}")

        payload = serializableCommand.toPayload(self._defaults)
        return self._buildFrame(serializableCommand.commandId, payload, isNewCommand)

    def _buildFrame(self, firmwareCommandId: FirmwareCommandId, payload: bytes, isNewCommand: bool = True) -> bytes:
        if isNewCommand:
            self._commandNumber = (self._commandNumber + 1) & 0xFFFFFFFF
        header = struct.pack('<BIH', firmwareCommandId.value, self._commandNumber, len(payload))
        return header + payload
