from dataclasses import dataclass
from enum import Enum
import numbers


class CommandId(Enum):
    STOP = 0    #Tells the machine to stop immediatly
    MOVE = 1    #Tells the machine to go to a setpoint
    PICK = 2    #Tells the machine to drop down, pick a piece, and go up
    PLACE = 3   #Tells the machine to drop down, place the piece, and go up
    HOME = 4    #Tells the machine to go home(x,y,z limit switches)
    EMPTY = 5   #Tells the machine to continue the current command

class Type(Enum):
    RESISTOR = 0    
    LED = 1



class StorageState(Enum):
    USING = 0   #Can be used by the slicer.
    IGNORE = 1  #Tells the slicer to ignore these components.
    EMPTY = 2   #The storage of these components is empty.

class MachineState(Enum):
    ERROR = 0
    READY = 1
    MOVING = 2
    PIKCING = 3
    PLACING = 4
    DISCONNECTED = 5 

class ControllerState(Enum):
    IDLE = 0
    RUNNING = 1
    MANUAL = 2
    PAUSE = 3
    DONE = 4

class TransitionRequest(Enum):
    TO_RUNNING = (1<<0)
    TO_MANUAL = (1<<1)
    TO_PAUSE = (1<<2)
    TO_IDLE = (1<<3)

@dataclass
class Position:
    """
    Class that represents a position in 3D space. It also handles z axis rotation

    Attributes:
        x (float): 
            The position in the x axis.
        y (float): 
            The position in the y axis.
        z (float):
            The position in the z axis.
        yaw (float):
            The rotation in the z axis.
    """
    x : float       
    y : float
    z : float 
    yaw : float

    def __add__(self, other):
        """Alows two position to be added together"""
        if not isinstance(other, Position):
            return NotImplemented
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        yaw = self.yaw + other.yaw
        return Position(x, y, z, yaw)
    
    def __mul__(self, other):
        """Allows a position to be multiplied by a scalar"""
        if not isinstance(other, numbers.Number) and not isinstance(other, bool):
            return NotImplemented
        x = self.x * other
        y = self.y * other
        z = self.z * other
        yaw = self.yaw * other
        return Position(x, y, z, yaw)

    def __rmul__(self, other):
        """Allows a position to be multiplied by a scalar"""
        return self.__mul__(other)
    
    def __eq__(self, other):
        """Verifies that two positions are exactly the same"""
        if not isinstance(other, Position):
            return NotImplemented
        x = self.x == other.x
        y = self.y == other.y
        z = self.z == other.z
        yaw = self.yaw == other.yaw
        return x and y and x and yaw 
    
    def toJSON(self):
        """
        Returns a list of the attributes of position so 
        that they are JSON serializable.
        """
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
    
    #Allows the object to be the key of a dictionary in the storage
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
    piece : Piece           
    deltaPos : Position     
    state : StorageState    
    quantity : int          
    automatic : bool        


@dataclass
class Command:

    commandId : CommandId
    velocity : float
    position : Position
    piece : Piece