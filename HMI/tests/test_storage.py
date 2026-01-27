import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from storage import Storage
from data import Position, Piece, Type, StorageState, StorageUnit


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.storage = Storage()




    def test_add_component(self):

        print("\nTEST STORAGE ADD COMPONENT")
        self.assertEqual(len(self.storage.components), 0)

        #one piece added
        piece =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="R_0805",
                  type=Type.RESISTOR,
                  value = '')
        deltaPos = Position(0,0,0,0)
        state = StorageState.USING
        quantity = 50
        automatic = False
        self.storage.addComponent(piece, deltaPos, state, quantity, automatic)
        self.assertEqual(len(self.storage.components), 1)
        storage_unit = self.storage.components[piece]
        self.assertEqual(storage_unit.piece.package, piece.package)
        self.assertEqual(storage_unit.deltaPos, deltaPos)
        self.assertEqual(storage_unit.state, state)
        self.assertEqual(storage_unit.quantity, quantity)
        self.assertEqual(storage_unit.automatic, automatic)



        #second piece added
        piece =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = '')
        deltaPos = Position(1,2,3,4)
        state = StorageState.EMPTY
        quantity = 60
        automatic = False
        self.storage.addComponent(piece, deltaPos, state, quantity, automatic)
        self.assertEqual(len(self.storage.components), 2)
        storage_unit = self.storage.components[piece]
        self.assertEqual(storage_unit.piece.package, piece.package)
        self.assertEqual(storage_unit.deltaPos, deltaPos)
        self.assertEqual(storage_unit.state, state)
        self.assertEqual(storage_unit.quantity, quantity)
        self.assertEqual(storage_unit.automatic, automatic)


        #third piece added
        piece = Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = '')
        deltaPos = Position(4,52,0,42)
        state = StorageState.EMPTY
        quantity = 98
        automatic = False
        self.storage.addComponent(piece, deltaPos, state, quantity, automatic)
        self.assertEqual(len(self.storage.components), 3)
        storage_unit = self.storage.components[piece]
        self.assertEqual(storage_unit.piece.package, piece.package)
        self.assertEqual(storage_unit.deltaPos, deltaPos)
        self.assertEqual(storage_unit.state, state)
        self.assertEqual(storage_unit.quantity, quantity)
        self.assertEqual(storage_unit.automatic, automatic)


        #duplicate piece added
        piece = Piece(position=Position(3, 26, 30.0, -95.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = '')
        deltaPos = Position(11,22,33,44)
        state = StorageState.USING
        quantity = 23
        automatic = True
        self.storage.addComponent(piece, deltaPos, state, quantity, automatic)
        self.assertEqual(len(self.storage.components), 3)
        storage_unit = self.storage.components[piece]
        self.assertEqual(storage_unit.piece.package, piece.package)
        self.assertEqual(storage_unit.deltaPos, deltaPos)
        self.assertEqual(storage_unit.state, state)
        self.assertEqual(storage_unit.quantity, quantity)
        self.assertEqual(storage_unit.automatic, automatic)

    


    def test_remove_component(self):
        print("\nTEST STORAGE REMOVE COMPONENT")
        piece1 =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="R_0805",
                  type=Type.RESISTOR,
                  value = '')
        piece2 =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="R_0603",
                  type=Type.RESISTOR,
                  value = '')
        piece3 = Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="LED_TEST",
                  type=Type.LED,
                  value = '')
        
        self.storage.components = {
            piece1 : StorageUnit(piece=piece1, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.USING, quantity=10, automatic=False),
            piece2 : StorageUnit(piece=piece2, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.USING, quantity=10, automatic=False),
            piece3 : StorageUnit(piece=piece3, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.USING, quantity=10, automatic=False)
        }

        #Removes a piece 
        self.storage.removeComponent(piece2)
        self.assertEqual(len(self.storage.components), 2)
        self.assertTrue(not piece2 in self.storage.components)

        #tries to remove the same piece 
        self.storage.removeComponent(piece2)
        self.assertEqual(len(self.storage.components), 2)

       


    def test_get_valid_components(self):
        print("\nTEST STORAGE VALID COMPONENT")
        piece1 =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="P1",
                  type=Type.RESISTOR,
                  value = '')
        piece2 =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="P2",
                  type=Type.RESISTOR,
                  value = '')
        piece3 = Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="P3",
                  type=Type.LED,
                  value = '')
        piece4 =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="P4",
                  type=Type.RESISTOR,
                  value = '')
        piece5 =Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="P5",
                  type=Type.RESISTOR,
                  value = '')
        piece6 = Piece(position=Position(1, 2, 0.0, -90.0000),
                  package="P6",
                  type=Type.LED,
                  value = '')
        
        self.storage.components = {
            piece1 : StorageUnit(piece=piece1, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.USING, quantity=10, automatic=False),
            piece2 : StorageUnit(piece=piece2, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.IGNORE, quantity=10, automatic=False),
            piece3 : StorageUnit(piece=piece3, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.USING, quantity=10, automatic=False),
            piece4 : StorageUnit(piece=piece4, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.EMPTY, quantity=10, automatic=False),
            piece5 : StorageUnit(piece=piece5, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.IGNORE, quantity=10, automatic=False),
            piece6 : StorageUnit(piece=piece6, deltaPos=Position(0,0,0,0), 
                                 state=StorageState.USING, quantity=10, automatic=False)
        }

        valid_components = self.storage.getValidComponents()
        self.assertEqual(len(valid_components), 3)
        for piece in valid_components:
            self.assertEqual(self.storage.components[piece].state, StorageState.USING)
        self.assertEqual(valid_components[0].package, "P1")
        self.assertEqual(valid_components[1].package, "P3")
        self.assertEqual(valid_components[2].package, "P6")

