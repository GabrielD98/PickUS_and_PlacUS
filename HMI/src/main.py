from file_interpreter import FileInterpreter

if __name__ == "__main__":
    print("Starting Program")

    try : 
        file = "../data/PCB_test-top.pos"
        interpreter = FileInterpreter()
        interpreter.readPositionFile(file)
    except Exception as e : 
        print(f"An error occured during the execution of the main program : {e}")

    print ("End of program")
    