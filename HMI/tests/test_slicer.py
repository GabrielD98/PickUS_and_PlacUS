import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest

from command_interface import HomeCommand, MoveCommand, PickCommand, PlaceCommand
from data import Position, Piece, Type, StorageState, StorageUnit
from slicer import Slicer
from storage import Storage


class TestSlicer(unittest.TestCase):
    def setUp(self):
        self.pieces = [
            Piece(position=Position(3, 2, 0.0, 90.0), package="1", type=Type.LED, value=''),
            Piece(position=Position(3, 3, 0.0, 45.0), package="1", type=Type.LED, value=''),
            Piece(position=Position(3, 4, 0.0, -90.0), package="1", type=Type.LED, value=''),
            Piece(position=Position(4, 2, 0.0, -90.0), package="2", type=Type.RESISTOR, value=''),
            Piece(position=Position(4, 3, 0.0, -90.0), package="2", type=Type.RESISTOR, value=''),
        ]

    def test_slice(self):
        piece1 = Piece(position=Position(1, 0, 0.0, -90.0), package="1", type=Type.RESISTOR, value='')
        piece2 = Piece(position=Position(2, 0, 0.0, 180.0), package="2", type=Type.LED, value='')

        storage = Storage()
        storage.components = {
            piece1: StorageUnit(piece=piece1, position=piece1.position, deltaPos=Position(0, 2, 0, 0), state=StorageState.USING, quantity=10, automatic=False),
            piece2: StorageUnit(piece=piece2, position=piece2.position, deltaPos=Position(0, 3, 0, 0), state=StorageState.USING, quantity=10, automatic=False),
        }

        slicer = Slicer()
        slicer.storage = storage

        commands = slicer.slice(self.pieces, Position(10, 20, 0, 0), Position(0, 0, -2, 0), 2.0)

        self.assertIsInstance(commands, list)
        self.assertEqual(len(commands), 31)

        self.assertIsInstance(commands[0], MoveCommand)
        self.assertIsInstance(commands[1], PickCommand)
        self.assertIsInstance(commands[4], PlaceCommand)
        self.assertEqual(commands[4].piece, self.pieces[0])
        self.assertIsInstance(commands[-1], HomeCommand)

        self.assertEqual(commands[0].position, Position(piece1.position.x, piece1.position.y, piece1.position.z, 0))
        self.assertEqual(commands[2].position, commands[0].position)


if __name__ == '__main__':
    unittest.main()
