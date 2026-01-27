from file_interpreter import FileInterpreter
from storage import Storage
from slicer import Slicer
from data import *
from unit_test import *
import unittest




if __name__ == "__main__":
    print("Starting Program")

    try : 
        #test_storage()

        unittest.main()
        #pieces = FileInterpreter().readPositionFile("../data/PCB_test-top.pos")
        #storage = Storage()
        #for piece in pieces:
        #    storage.addComponent(piece=piece,
        #                        deltaPos=Position(0,2,0,0),
        #                        state=StorageState.USING,
        #                        quantity=100,
        #                        automatic=False)
        #    
        #Slicer("../data/test.json").slice(pieces, Position(2,3,0,0), Position(1,1,0,0), Position(0,0,-3,0))

        

    except Exception as e : 
        print(f"An error occured during the execution of the main program : {e}")

    print ("End of program")
    