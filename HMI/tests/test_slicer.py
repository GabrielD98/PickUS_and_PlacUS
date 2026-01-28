import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from slicer import Slicer
from storage import Storage
from data import Position, Piece, Type, StorageState, StorageUnit, Command
import json


class TestSlicer(unittest.TestCase):
    def setUp(self):
        self.pieces = [
            Piece(position=Position(3, 2, 0.0, 90.0000),
                  package="1",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(3, 3, 0.0, 45.0000),
                  package="1",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(3, 4, 0.0, -90.0000),
                  package="1",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(4, 2, 0.0, -90.0000),
                  package="2",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(4, 3, 0.0, -90.0000),
                  package="2",
                  type=Type.RESISTOR,
                  value = '')
        ]




    def test_slice(self):
        print("\nTEST SLICE")
        piece1 =Piece(position=Position(1, 0, 0.0, -90.0000),
                  package="1",
                  type=Type.RESISTOR,
                  value = '')
        piece2 = Piece(position=Position(2, 0, 0.0, 180.0000),
                  package="2",
                  type=Type.LED,
                  value = '')
        storage = Storage()
        delta_pos_p1 = Position(0,2,0,0)
        delta_pos_p2 = Position(0,3,0,0)
        storage.components = {
            piece1 : StorageUnit(piece=piece1, deltaPos=delta_pos_p1, 
                                 state=StorageState.USING, quantity=10, automatic=False),
            piece2 : StorageUnit(piece=piece2, deltaPos=delta_pos_p2, 
                                 state=StorageState.USING, quantity=10, automatic=False)
        }

        file_path = "tests/data/testslicer.json"
        slicer = Slicer()
        slicer_speed = 2.0
        offset = Position(10, 20, 0, 0)
        z_offset = Position(0, 0, -2, 0)
        slicer.slice(self.pieces, offset, z_offset, file_path, slicer_speed)
        
        data = {}
        try:
            with open(file_path, "r") as file:
                data = json.load(file)

        except Exception:
            self.assertTrue(False) #failed to open, fails the the test

        #PIECE 1

        #1rst command
        position = data["component1"]["1"]["position"]
        result = (piece1.position + offset).toJSON()
        self.assertListEqual(position, result)     

        command = data["component1"]["1"]["command"]   
        self.assertEqual(command, Command.MOVE.value) 

        speed = data["component1"]["1"]["speed"]   
        self.assertEqual(speed, slicer_speed) 

        command = data["component1"]["2"]["command"]   
        self.assertEqual(command, Command.PICK.value) 

        position = data["component1"]["2"]["position"]
        result = (piece1.position + offset + z_offset).toJSON()
        self.assertListEqual(position, result)  

        command = data["component1"]["3"]["command"]   
        self.assertEqual(command, Command.MOVE.value) 

        position = data["component1"]["3"]["position"]
        result = (self.pieces[0].position + offset).toJSON()
        self.assertListEqual(position, result) 

        command = data["component1"]["4"]["command"]   
        self.assertEqual(command, Command.PLACE.value) 

        position = data["component1"]["4"]["position"]
        result = (self.pieces[0].position + offset + z_offset).toJSON()
        self.assertListEqual(position, result) 


        #2nd command (ensures that the deltaPos keeps going)
        position = data["component2"]["1"]["position"]
        result = (piece1.position + offset + storage.components[piece1].deltaPos).toJSON()
        self.assertListEqual(position, result)     

        #3nd command (ensures that the deltaPos keeps going)
        position = data["component3"]["1"]["position"]
        result = (piece1.position + offset + (2 * storage.components[piece1].deltaPos)).toJSON()
        self.assertListEqual(position, result)


        #PIECE 2

        #1rst command
        position = data["component4"]["1"]["position"]
        result = (piece2.position + offset).toJSON()
        self.assertListEqual(position, result)     

        command = data["component4"]["1"]["command"]   
        self.assertEqual(command, Command.MOVE.value) 

        speed = data["component4"]["1"]["speed"]   
        self.assertEqual(speed, slicer_speed) 

        command = data["component4"]["2"]["command"]   
        self.assertEqual(command, Command.PICK.value) 

        position = data["component4"]["2"]["position"]
        result = (piece2.position + offset + z_offset).toJSON()
        self.assertListEqual(position, result)  

        command = data["component4"]["3"]["command"]   
        self.assertEqual(command, Command.MOVE.value) 

        position = data["component4"]["3"]["position"]
        result = (self.pieces[3].position + offset).toJSON()
        self.assertListEqual(position, result) 

        command = data["component4"]["4"]["command"]   
        self.assertEqual(command, Command.PLACE.value) 

        position = data["component4"]["4"]["position"]
        result = (self.pieces[3].position + offset + z_offset).toJSON()
        self.assertListEqual(position, result) 


        #2nd command (ensures that the deltaPos keeps going)
        position = data["component5"]["1"]["position"]
        result = (piece2.position + offset + storage.components[piece2].deltaPos).toJSON()
        self.assertListEqual(position, result)     


        #test for going home
        position = data["home"]["1"]["position"]
        result = offset.toJSON()
        self.assertListEqual(position, result)     

        command = data["home"]["1"]["command"]   
        self.assertEqual(command, Command.MOVE.value) 

        speed = data["home"]["1"]["speed"]   
        self.assertEqual(speed, slicer_speed) 



        
            