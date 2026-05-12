from dataclasses import dataclass, field
from enum import Enum, IntFlag
import numbers
from pathlib import Path

MAX_SPEED = 100 #mm/s
MAX_TOOLHEAD = 1
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
CALIB_PATH = str(DATA_DIR / 'calib.json')


def get_status_packet_format() -> str:
    """Build the packed ESP32 status payload format from the configured toolhead count."""
    return '<BBllll' + f'{MAX_TOOLHEAD}f' + f'{MAX_TOOLHEAD}?' + '?'


class Type(Enum):
    RESISTOR = 0
    LED = 1


class StorageState(Enum):
    USING = 0
    IGNORE = 1
    EMPTY = 2


class MachineState(Enum):
    ERROR = 0
    READY = 1
    RUNNING = 2


class ControllerState(Enum):
    IDLE = 0
    RUNNING = 1
    MANUAL = 2
    PAUSE = 3
    DONE = 4


class TransitionRequest(IntFlag):
    TO_RUNNING = (1 << 0)
    TO_MANUAL = (1 << 1)
    TO_PAUSE = (1 << 2)
    TO_IDLE = (1 << 3)


@dataclass
class Position:
    """Represents a 3D position with yaw rotation."""
    x: float
    y: float
    z: float
    yaw: float

    def __add__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x + other.x, self.y + other.y, self.z + other.z, self.yaw + other.yaw)

    def __sub__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x - other.x, self.y - other.y, self.z - other.z, self.yaw - other.yaw)

    def __mul__(self, other):
        if isinstance(other, Position):
            return Position(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z,
                self.yaw * other.yaw,
            )

        if isinstance(other, (numbers.Number, bool)):
            return Position(
                self.x * other,
                self.y * other,
                self.z * other,
                self.yaw * other,
            )

        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return (
            self.x == other.x
            and self.y == other.y
            and self.z == other.z
            and self.yaw == other.yaw
        )

    def toJSON(self):
        return [self.x, self.y, self.z, self.yaw]


@dataclass
class Piece:
    """
    Class that represents a component handled by the pick and place.

    Attributes:
        position (Position): 
            The position of the piece on the PCB or storage, ignores the offset.
        package (str): 
            The string package read by the .pos file of Kicad. It is used as an ID.
        type (Type):
            The type of the component (ex : resistor, LED).
        value (str):
            The value of the component  (ex : 100 Ohm for a resistor)
    """
    position : Position     
    package : str           
    type : Type             
    value : str             

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented
        return self.package == other.package

    def __hash__(self):
        return hash(self.package)


@dataclass
class StorageUnit:
    """
    Class that represents the storage of a certain component.

    Attributes:
        piece (Piece): 
            The component in this storage unit.
        deltaPos (Position): 
            TThe offset between all pieces on this unit.
        state (StorageState):
            The state of the unit, tells the HMI or the slicer if this unit is available.
        quantity (int):
            The amount of components stored in this unit.
        automatic (bool):
            Is the feeder automatic or not.
    """
    
    piece: Piece
    deltaPos: Position
    state: StorageState
    quantity: int
    position: Position = field(default_factory=lambda: Position(0, 0, 0, 0))
    automatic: bool = False
    toolhead_index: int = 0
