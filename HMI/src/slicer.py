from typing import Any, List
import os
from file_interpreter import FileInterpreter
from storage import Storage
from data import *

#TODO ficiher de constante?
Z_SPEED = 1.0 #cm/s

class Slicer :
    """
    Class that handles all the set point that the Pick & Place has to travel to
    to successfully place all of the components. 

    Attributes:
        storage (Storage): 
            The storage of all the components to be placed 

    """


    def __init__(self ):
        self.storage = Storage()    



    #TODO revalider les units de la vitesse
    def slice(self, pieces:List[Piece], offset:Position, z_offset:Position, speed:float) -> List[Command]:
        """
        Generates all of the commands and setpoints for the placement of components.
        Returns a list of Command objects to be used by the controller class.

        Parameters:
            piece (Piece): The list of all the pieces to be placed.
            offset (Position): The offset between the position of the origin
                                of the PCB vs the origin of the machine.
                                Has to be generated in the calibration step. 
            z_offset (Position): The offset of the z axis when the prehencer is
                                fully retracted vs when z position of the PCB. Allows
                                the machine to know the height of the placement.
                                Has to be generated in the calibration step.
            speed (float): The speed of the movement of the pcb machine (cm/s)
        
        Returns:
            List[Command]: The list of commands to execute for placing all components.
        """


        #gets a list of all the available piece in the storage
        available = self.storage.getValidComponents()
        storage_offset:dict[Piece, Position] = {}
        for piece in available:
            storage_offset[piece] = Position(0, 0, 0, 0)

        commands:List[Command] = []

        for piece in pieces:
            
            if piece not in available:
                continue
            
            #for each piece, move towards its place in the storage, 
            #pick it, move towards the placement zone, and place it
            pick_position = self.storage.components[piece].piece.position
            
            # Move to storage position
            commands.append(Command(
                commandId=CommandId.MOVE,
                velocity=speed,
                position=pick_position + offset + storage_offset[piece],
                piece=piece
            ))
            
            # Pick the piece
            commands.append(Command(
                commandId=CommandId.PICK,
                velocity=Z_SPEED,
                position=pick_position + z_offset + offset + storage_offset[piece],
                piece=piece
            ))
            
            # Move to placement position
            commands.append(Command(
                commandId=CommandId.MOVE,
                velocity=speed,
                position=piece.position + offset,
                piece=piece
            ))
            
            # Place the piece
            commands.append(Command(
                commandId=CommandId.PLACE,
                velocity=Z_SPEED,
                position=piece.position + z_offset + offset,
                piece=piece
            ))

            #updates the new position of the piece in the storage if the storage is not auto
            if not self.storage.components[piece].automatic :
                storage_offset[piece] = storage_offset[piece] + self.storage.components[piece].deltaPos

        #when all is done, move to 'home' position
        commands.append(Command(
            commandId=CommandId.HOME,
            velocity=speed,
            position=None,
            piece=None
        ))
        
        return commands