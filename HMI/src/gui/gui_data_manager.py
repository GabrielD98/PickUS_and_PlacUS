from controller import Controller
from typing import List
from data import Command, Position, TransitionRequest

#TODO cettte class probablement useless, a voir si on switch direct vers le controller. Jle grade pour simplifier


class GuiDataManager:
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self.initialized = True

        self.controller = Controller() 
        self.commands:List[Command] = []




    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GuiDataManager, cls).__new__(cls)
        return cls.instance



    def get_machine_state(self):
        return self.controller.getState()
    

    def get_gripper_position(self) -> Position:
        return self.controller.getState()[2]
    

    def queue_command(self, command:Command):
        self.controller.queueCommand(command)


    def set_pnp_commands(self, command:Command):
        self.commands = command 

    
    def start_pnp(self):
        self.controller.queueCommands(self.commands)


    def pause_pnp(self):
        self.controller.requestTransition(TransitionRequest.TO_PAUSE)


    def stop_pnp(self):
        pass #TODO Eloi?



    def continue_pnp(self):
        self.controller.requestTransition(TransitionRequest.TO_RUNNING)



    def connect_to_pnp(self):
        self.controller.connectionToMachine()