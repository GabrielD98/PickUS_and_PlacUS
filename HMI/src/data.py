from dataclasses import dataclass
from enum import Enum


class Type(Enum):
    RESISTOR = 0    
    LED = 1



class StorageState(Enum):
    USING = 0   #Can be used by the slicer.
    IGNORE = 1  #Tells the slicer to ignore these components.
    EMPTY = 2   #The storage of these components is empty.




@dataclass
class Position:
    x : float       
    y : float
    z : float 
    rotation : float




@dataclass
class Piece:
    position : Position     #The position of the piece on the PCB, ignores the offset.
    package : str           #The string package read by the .pos file of Kicad.
    type : Type             #The type of the component (ex : resistor, LED).
    value : str             #The value of the component  (ex : 100 Ohm for a resistor)

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented
        return self.package == other.package
    
    #Allows the object to be the key of a dictionary in the storage unit
    def __hash__(self):
        return hash(self.package)




@dataclass
class StorageUnit:
    piece : Piece           #The piece of this storage unit.
    deltaPos : Position     #The offset between all pieces on this unit.
    state : StorageState    #The state of the unit, tells the HMI if this unit is available.
    quantity : int          #The amount of components stored.
    automatic : bool        #Is the feeder automatic or not.
