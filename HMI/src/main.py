from file_interpreter import FileInterpreter
from storage import Storage
from slicer import Slicer
from data import *
from controller import Controller



test = Controller()

if __name__ == "__main__":
    print("Starting Program")

    try : 

        
        test.connectionToMachine("COM19",115200)

        

    except Exception as e : 
        print(f"An error occured during the execution of the main program : {e}")

    print ("End of program")
    