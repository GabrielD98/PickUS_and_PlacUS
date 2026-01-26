from file_interpreter import FileInterpreter
from storage import Storage
from data import *
from unit_test import *




if __name__ == "__main__":
    print("Starting Program")

    try : 
        test_storage()

        

    except Exception as e : 
        print(f"An error occured during the execution of the main program : {e}")

    print ("End of program")
    