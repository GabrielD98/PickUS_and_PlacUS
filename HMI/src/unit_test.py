from typing import List
from file_interpreter import FileInterpreter
from storage import Storage
from data import *

def test_storage():

    file = "../data/PCB_test-top.pos"
    interpreter = FileInterpreter()
    pieces = interpreter.readPositionFile(file)

    storage = Storage()
    for piece in pieces:
        storage.addComponent(piece=piece,
                            deltaPos=Position(0,0,0,0),
                            state=StorageState.USING,
                            quantity=100,
                            automatic=False)
    
    storage.components[pieces[1]].state = StorageState.EMPTY #for future test
    print("TEST ADD COMPONENT")
    print("------------------")
    for key in storage.components:
        unit = storage.components[key]
        print(unit.piece.package, " : ")
        print("     -",  unit)
        print()
    print()
    print()

    print("TEST GET VALID COMPONENT")
    print("------------------------")
    valid_comp = storage.getValidComponents()
    for piece in valid_comp:
        print(piece)
        print()
    print()
    print()


    print("TEST REMOVE COMPONENT : ", pieces[12].package)
    print("------------------")
    storage.removeComponent(storage.components[pieces[12]].piece)
    for key in storage.components:
        unit = storage.components[key]
        print(unit.piece.package, " : ")
        print("     -",  unit)
        print()
    print()
    print()


def test_file_interpreter():
    print("TEST FILE INTERPRETER")
    print("---------------------")
    file = "../data/PCB_test-top.pos"
    interpreter = FileInterpreter()
    pieces = interpreter.readPositionFile(file)
    for piece in pieces:
        print(piece)
    print()
    print()