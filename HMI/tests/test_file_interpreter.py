import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from file_interpreter import FileInterpreter
from data import Position, Piece, Type


class TestFileInterpreter(unittest.TestCase):
    def setUp(self):
        print("\n\n///////////////////////////////")
        print("//   TEST FILE INTERPRETER   //")
        print("///////////////////////////////\n")

        self.fileInterpreter = FileInterpreter()
        self.file = "tests/data/testKicad.txt"

        self.pieces = [
            Piece(position=Position(66.0000, -36.0000, 0.0, 90.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(45.5000, -46.0000, 0.0, 45.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(50.0000, -5.50000, 0.0, 0.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(76.5000, -65.0000, 0.0, -90.0000),
                  package="R_0805",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(76.5000, -69.0000, 0.0, -90.0000),
                  package="R_0805",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(69.5000, -65.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(69.5000, -69.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(71.5000, -73.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(34.5000, -77.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(32.5000, -81.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = '')
        ]


    def test_reading(self):

        print("TEST FILE READING")
        pieces = self.fileInterpreter.readPositionFile(self.file)

        self.assertEqual(len(pieces), len(self.pieces))
        for index in range(0, len(pieces)) :
            self.assertEqual(pieces[index].package, self.pieces[index].package)
            self.assertEqual(pieces[index].type, self.pieces[index].type)
            self.assertEqual(pieces[index].value, self.pieces[index].value)
            self.assertEqual(pieces[index].position, self.pieces[index].position)
        