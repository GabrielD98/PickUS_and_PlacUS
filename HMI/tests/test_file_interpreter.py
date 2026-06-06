import sys
import os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from file_interpreter import FileInterpreter
from data import Position, Piece, Type


class TestFileInterpreter(unittest.TestCase):
    def setUp(self):

        self.fileInterpreter = FileInterpreter()
        self.file = Path(__file__).parent / "data" / "testKicad.txt"
        self.referenceRef = "J1"

        self.pieces = [
            Piece(position=Position(9.0000, -1.0000, 0.0, 90.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(-11.5000, -11.0000, 0.0, 45.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(-7.0000, 29.5000, 0.0, 0.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = ''),
            Piece(position=Position(19.5000, -30.0000, 0.0, -90.0000),
                  package="R_0805",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(19.5000, -34.0000, 0.0, -90.0000),
                  package="R_0805",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(12.5000, -30.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(12.5000, -34.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(14.5000, -38.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(-22.5000, -42.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = ''),
            Piece(position=Position(-24.5000, -46.0000, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = '')
        ]


    def test_reading(self):

        print("TEST FILE READING")
        pieces = self.fileInterpreter.readPositionFile(self.file, self.referenceRef)

        self.assertEqual(len(pieces), len(self.pieces))
        for index in range(0, len(pieces)) :
            self.assertEqual(pieces[index].package, self.pieces[index].package)
            self.assertEqual(pieces[index].type, self.pieces[index].type)
            self.assertEqual(pieces[index].value, self.pieces[index].value)
            self.assertEqual(pieces[index].position, self.pieces[index].position)
        