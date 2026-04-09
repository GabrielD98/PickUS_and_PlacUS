import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from slicer import Slicer
from storage import Storage
from data import Position, Piece, Type, StorageState, StorageUnit, Command, CommandId


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

        slicer = Slicer()
        slicer.storage = storage
        slicer_speed = 2.0
        offset = Position(10, 20, 0, 0)
        z_offset = Position(0, 0, -2, 0)
        commands = slicer.slice(self.pieces, offset, z_offset, slicer_speed)
        
        # Verify we got a list of Command objects
        self.assertIsInstance(commands, list)
        self.assertTrue(len(commands) > 0)
        self.assertIsInstance(commands[0], Command)

        #PIECE 1 (3 LEDs with package "1")
        # Each piece has 4 commands: MOVE, PICK, MOVE, PLACE
        # So piece 1 commands are at indices 0-3

        #1st command - MOVE to storage
        cmd = commands[0]
        self.assertEqual(cmd.commandId, CommandId.MOVE)
        self.assertEqual(cmd.velocity, slicer_speed)
        self.assertEqual(cmd.position, piece1.position + offset)
        self.assertEqual(cmd.piece, self.pieces[0])  # First LED piece

        #2nd command - PICK
        cmd = commands[1]
        self.assertEqual(cmd.commandId, CommandId.PICK)
        self.assertEqual(cmd.position, piece1.position + offset + z_offset)

        #3rd command - MOVE to placement
        cmd = commands[2]
        self.assertEqual(cmd.commandId, CommandId.MOVE)
        self.assertEqual(cmd.position, self.pieces[0].position + offset)

        #4th command - PLACE
        cmd = commands[3]
        self.assertEqual(cmd.commandId, CommandId.PLACE)
        self.assertEqual(cmd.position, self.pieces[0].position + offset + z_offset)
        # Verify x,y match between MOVE and PLACE
        self.assertEqual(commands[3].position.x, commands[2].position.x)
        self.assertEqual(commands[3].position.y, commands[2].position.y)

        #2nd piece commands (indices 4-7) - ensures that the deltaPos keeps going
        cmd = commands[4]
        self.assertEqual(cmd.commandId, CommandId.MOVE)
        self.assertEqual(cmd.position, piece1.position + offset + storage.components[piece1].deltaPos)
        # Verify x,y match between MOVE and PICK
        self.assertEqual(commands[4].position.x, commands[5].position.x)
        self.assertEqual(commands[4].position.y, commands[5].position.y)

        #3rd piece commands (indices 8-11) - ensures that the deltaPos keeps going
        cmd = commands[8]
        self.assertEqual(cmd.commandId, CommandId.MOVE)
        self.assertEqual(cmd.position, piece1.position + offset + (2 * storage.components[piece1].deltaPos))
        # Verify x,y match between MOVE and PICK
        self.assertEqual(commands[8].position.x, commands[9].position.x)
        self.assertEqual(commands[8].position.y, commands[9].position.y)

        #PIECE 2 (2 RESISTORs with package "2")
        # 4th component commands (indices 12-15)

        #1st command - MOVE to storage
        cmd = commands[12]
        self.assertEqual(cmd.commandId, CommandId.MOVE)
        self.assertEqual(cmd.velocity, slicer_speed)
        self.assertEqual(cmd.position, piece2.position + offset)
        self.assertEqual(cmd.piece, self.pieces[3])  # First RESISTOR piece

        #2nd command - PICK
        cmd = commands[13]
        self.assertEqual(cmd.commandId, CommandId.PICK)
        self.assertEqual(cmd.position, piece2.position + offset + z_offset)

        #3rd command - MOVE to placement
        cmd = commands[14]
        self.assertEqual(cmd.commandId, CommandId.MOVE)
        self.assertEqual(cmd.position, self.pieces[3].position + offset)

        #4th command - PLACE
        cmd = commands[15]
        self.assertEqual(cmd.commandId, CommandId.PLACE)
        self.assertEqual(cmd.position, self.pieces[3].position + offset + z_offset)

        #5th component commands (indices 16-19) - 2nd RESISTOR, ensures that the deltaPos keeps going
        cmd = commands[16]
        self.assertEqual(cmd.commandId, CommandId.MOVE)
        self.assertEqual(cmd.position, piece2.position + offset + storage.components[piece2].deltaPos)

        #test for going home - should be the last command
        cmd = commands[-1]
        self.assertEqual(cmd.commandId, CommandId.HOME)
        self.assertEqual(cmd.velocity, slicer_speed)
        self.assertIsNone(cmd.position)  # HOME command uses None position (uses limit switches)
        self.assertIsNone(cmd.piece)  # Home command has no associated piece 



        
            