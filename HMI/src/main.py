from file_interpreter import FileInterpreter
from storage import Storage
from slicer import Slicer
from data import *
from gui.interface import Interface
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys



if __name__ == "__main__":
    print("Starting Program")

    try : 
        app = QApplication(sys.argv)
        window = Interface()
        window.show()
        app.exec()



    except Exception as e : 
        print(f"An error occured during the execution of the main program : {e}")

    print ("End of program")
    