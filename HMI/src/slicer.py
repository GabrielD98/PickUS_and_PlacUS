from typing import Any, List
import os
from file_interpreter import FileInterpreter
from storage import Storage
from data import *
from geometry import CartesianVelocity, dimensionLimits
from command_interface import HomeCommand, MoveCommand, PickCommand, PlaceCommand, DEFAULT_HOME_VELOCITY

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



    def slice(self, pieces:List[Piece], offset:Position, z_offset:Position, speed:float) -> List[MoveCommand | PickCommand | PlaceCommand | HomeCommand]:
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
            speed (float): The speed of the movement of the pcb machine (mm/s)
        
        Returns:
            List[Command]: The list of commands to execute for placing all components.
        """


        #gets a list of all the available piece in the storage
        available = self.storage.getValidComponents()
        storage_offset:dict[Piece, Position] = {}
        for piece in available:
            storage_offset[piece] = Position(0, 0, 0, 0)

        commands:List[MoveCommand | PickCommand | PlaceCommand | HomeCommand] = []

        #commands.append(Command(
        #    commandId=CommandId.HOME,
        #    velocity=speed,
        #    position=None,
        #    piece=None
        #))
        z_mask = Position(1,1,0,1)
        yaw_mask = Position(1,1,1,0)
        for piece in pieces:
            
            if piece not in available:
                continue
            
            #for each piece, move towards its place in the storage, 
            #pick it, move towards the placement zone, and place it
            pick_position = self.storage.components[piece].position
            pick_position = dimensionLimits(pick_position)
            toolheadIndex = self.storage.components[piece].toolhead_index
            

            #PICK
            # Move to storage position
            commands.append(MoveCommand(
                position=dimensionLimits(((pick_position*z_mask) + storage_offset[piece])*yaw_mask),
                velocity=CartesianVelocity.uniform(speed),
            ))
            
            # Pick the piece
            commands.append(PickCommand(toolheadIndex=toolheadIndex))

            commands.append(MoveCommand(
                position=dimensionLimits(((pick_position*z_mask) + storage_offset[piece])*yaw_mask),
                velocity=CartesianVelocity.uniform(speed),
            ))

            yaw = (piece.position.yaw - pick_position.yaw) % 360 
            if abs(yaw) > 180:
                if yaw < 0:
                    yaw = yaw + 360
                else:
                    yaw = yaw - 360
            rotation = Position(0, 0, 0, yaw)
            
            # Move to placement position
            commands.append(MoveCommand(
                position=dimensionLimits((piece.position+ offset)*z_mask*yaw_mask + rotation),
                velocity=CartesianVelocity.uniform(speed),
            ))

            
            # Place the piece
            commands.append(PlaceCommand(toolheadIndex=toolheadIndex, piece=piece))

            # Move to placement position
            commands.append(MoveCommand(
                position=dimensionLimits((piece.position+ offset)*z_mask*yaw_mask + rotation),
                velocity=CartesianVelocity.uniform(speed),
            ))          
            

            #updates the new position of the piece in the storage if the storage is not auto
            if not self.storage.components[piece].automatic :
                storage_offset[piece] = storage_offset[piece] + self.storage.components[piece].deltaPos

        #when all is done, move to 'home' position
        commands.append(HomeCommand(DEFAULT_HOME_VELOCITY))
        
        return commands