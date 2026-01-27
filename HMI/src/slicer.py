from typing import Any, List
import os
import json
from file_interpreter import FileInterpreter
from storage import Storage
from data import *

#TODO ficiher de constante?
Z_SPEED = 1.0 #cm/s

class Slicer :
    
    def __init__(self, JSON_path:str):
        self.JSON_path = JSON_path
        self.file_interpreter = FileInterpreter()
        self.storage = Storage()    

        self.speed:float = 1.0 #cm/s




    def slice(self, pieces:List[Piece], offset:Position, pick_position:Position, z_offset:Position):
        available = self.storage.getValidComponents()
        storage_offset:dict[Piece, Position] = {}
        for piece in available:
            storage_offset[piece] = Position(0, 0, 0, 0)
        #print(available)
        piece_id:int = 1
        commands:dict[str, dict] = {}
        home = Position(0,0,0,0)

        for piece in pieces:
            
            if piece not in available:
                continue
            
            piece_pos:Position = piece.position + offset
            pick_offset = Position(0,-1,0,0) #TODO dealer pick ofset
            commands[f"component{piece_id}"] = {
                1 : {
                    "command" : Command.MOVE.value,
                    "speed" : self.speed,
                    "position" : (pick_position + offset + storage_offset[piece]).toJSON()
                }, 
                2 : {
                    "command" : Command.PICK.value, 
                    "speed" : Z_SPEED, 
                    "position" : (pick_position + pick_offset + offset).toJSON()
                }, 
                3 : {
                    "command" : Command.MOVE.value,
                    "speed" : self.speed,
                    "position" : (piece_pos + offset).toJSON()
                },
                4 : {
                    "command" : Command.PLACE.value, 
                    "speed" : Z_SPEED,
                    "position" : (piece_pos + z_offset + offset).toJSON()
                }
            }
            storage_offset[piece] = storage_offset[piece] + self.storage.components[piece].deltaPos
            piece_id += 1

        commands["home"] = {
            1 : {
                "command" : Command.MOVE.value, 
                "speed" : self.speed,
                "position" : (home + offset).toJSON()
            }
        }
        #print(commands)
        self.writeToJSON(commands)
            

        


    def addPiece(self):
        pass




    def writeToJSON(self, data:dict[str, Any]):
        with open(self.JSON_path, 'w') as f:
            json.dump(data, f, indent=4)