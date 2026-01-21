from dataclasses import dataclass
from enum import Enum


class Type(Enum):
    RESISTOR = 0
    DEL = 1


@dataclass
class Position:
    x : float
    y : float
    z : float 
    rotation : float


@dataclass
class Piece:
    position : Position
    package : str
    type : Type
    value : str

