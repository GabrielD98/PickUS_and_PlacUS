import time

from controller import Controller
from typing import List
from data import MAX_SPEED, Command, CommandId, Position, TransitionRequest, MachineState
import threading
#TODO cettte class probablement useless, a voir si on switch direct vers le controller. Jle grade pour simplifier


class GuiDataManager:
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self.initialized = True

        self.controller = Controller() 
        self.commands:List[Command] = []
        self.blocked = False
        self.homed = False




    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GuiDataManager, cls).__new__(cls)
        return cls.instance



    def get_machine_state(self) -> MachineState:
        return self.controller.getState()[1]
    

    def get_gripper_position(self) -> Position:
        return self.controller.getState()[2]
    

    def queue_command(self, command:Command):
        if self.blocked:
            return
        self.controller.queueCommand(command)


    def set_pnp_commands(self, command:Command):
        if self.blocked:
            return
        self.commands = command 

    
    def start_pnp(self):
        if self.blocked:
            return
        self.controller.queueCommands(self.commands)


    def pause_pnp(self):
        self.controller.requestTransition(TransitionRequest.TO_PAUSE)


    def stop_pnp(self):
        pass #TODO Eloi?




    def homing_thread(self, ending_function = None):
        self.blocked = True
        home_cmd = Command(CommandId.HOME,
            velocity=MAX_SPEED*0.5,
            position=None,
            piece=None)
        self.controller.queueCommand(home_cmd)

        while not self.get_machine_state() == MachineState.READY:
            time.sleep(0.5)

        if ending_function is not None:
            ending_function()
        self.homed = True
        self.blocked = False
        


    def go_home(self, ending_function):
        if self.blocked :
            return
        home_thread = threading.Thread(target=self.homing_thread,  args=(ending_function,))
        home_thread.start()



    def continue_pnp(self):
        self.controller.requestTransition(TransitionRequest.TO_RUNNING)



    def connect_to_pnp(self):
        self.controller.connectionToMachine(comPort = "COM8", baudrate = 115200)