import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
	QVBoxLayout,
    QPushButton,
    QWidget, 
	QLabel,
    QScrollArea
)

import utils
from data import Piece, Position
from slicer import Slicer
from storage import Storage
from controller import Controller
from gui.tab_widget import TabWidget

class SliceInfoWidget(QWidget):
    """
    Widget for displaying and managing slicing information for Pick and Place operations.
    Handles slicing commands, displays command details, and emits signals when slicing is done.

    Attributes:
        calibrationPos (Position):
            A reference to the position of the head of the gripper. Allows the main UI to keep
            this position when the calibration is done.
        _slicer (Slicer):
            slicer object to allow the user to manually toggle the slice generation.
        _controller (Controller):
            Controller thats allows this object to send commands to the machine
            and receives information from it.
        _storage (Storage):
            instance of the storage data initialise by the user in the calibration phase. 
        __pieces (List[Piece]):
            list of all the piece to be placed by the PnP. Needed for the slicing logic.
        _commands(List[QLabel]):
            the list of all the command written in the QLabels. Allows the HMI to keep track 
            of the current command label, in a cleaner way than with the scroll area
        __currentCommandIndex (int):
            the index of the current command being executed. 
    """
    sliceDoneSignal = pyqtSignal(bool) 


    def __init__(self, calibrationPos:Position):
        """
        Initialize the SliceInfoWidget, set up the UI, and prepare slicing controls.
        
        Args:
            calibration_pos (Position): 
            A reference to the calibration position for slicing. To be saved by the main UI.
            #TODO signal would be better maybe
        """
        super().__init__()

        #main relevant attributes 
        self.calibrationPos = calibrationPos
        self._slicer = Slicer()
        self._controller = Controller()
        self._storage = Storage()
        self._pieces:List[Piece] = None
        self._commands:List[QLabel] = []
        self._currentCommandIndex:int = -1
        
        #global layout of this widget
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        #actionnable widget
        self._sliceButton = QPushButton("Slice")
        self._sliceButton.clicked.connect(self.slice)
        self._sliceButton.setEnabled(False)
        layout.addWidget(self._sliceButton)

        #Area that displays all of the steps of the slicing
        #self.scrollArea = QScrollArea(self)
        #layout.addWidget(self.scrollArea)
        #self.scrollArea.setWidgetResizable(True)
        #scrollContent = QWidget(self.scrollArea)

        self.tabs = TabWidget(self)
        #self.scrollLayout = QVBoxLayout(scrollContent)
        #scrollContent.setLayout(self.tabs.scrollLayout)
        #self.scrollArea.setWidget(scrollContent)


        self.index = 0
        layout.addWidget(self.tabs)

        

       

    def slice(self):
        """
        Perform slicing on the provided pieces, update the controller with commands,
        and display command details in the widget. Emits a signal when slicing is done.
        """
        
        commands = self._slicer.slice(self._pieces,
                                          self.calibrationPos,    #TODO calbiration pos of PCB
                                          Position(0,0,0,0),   #TODO offset du z
                                          150)              #TODO wtf is this
        
        self._controller.setPnpCommands(commands)

        #displays all of the generated steps in the scroll layout
        utils.clearLayout(self.tabs.scrollLayout)
        for command in commands:
            position = command.position

            commandInfo = f"Command : {command.commandId} | " 
            pieceInfo = ""
            if command.piece is not None:
                pieceInfo = f"Piece : {command.piece.package} | "
            positionInfo = ""
            if command.piece is not None:
                positionInfo = (f"Position : {round(position.x, 2)} " 
                f"{round(position.y, 2)}  {round(position.z, 2)}  {round(position.yaw, 2)} | ")
            speedInfo = f"Speed : {command.velocity}"

            comLabel = QLabel(commandInfo+pieceInfo+positionInfo+speedInfo)
            self._commands.append(comLabel)

        #tells the command widget that the slicing is done
        self._currentCommandIndex = -1
        self.sliceDoneSignal.emit(True)
        self.tabs.scrollLayout.addWidget(comLabel)

        self.show_graph()




    def setPieces(self, pieces:List[Piece]):
        """
        Set the list of pieces to be sliced.
        
        Args:
            pieces (List[Piece]): The pieces to slice.
        """
        self._pieces = pieces




    def enableSlicing(self):
        """
        Enable the slicing button, allowing the user to start slicing.
        """
        self._sliceButton.setEnabled(True)




    def reset(self):
        """
        Reset the widget by clearing the layout and disabling the slice button.
        """
        utils.clearLayout(self.tabs.scrollLayout)
        self._sliceButton.setEnabled(False)



    def onNextCommand(self):
        """
        Called when the next command is poped from the queue in the controller.
        Allows the HMI to display the current command executed by the PnP.
        """
        try :
            if self._currentCommandIndex >= 0:
                self._commands[self._currentCommandIndex].setStyleSheet("color: black;")
            
            self._currentCommandIndex += 1
            if self._currentCommandIndex < len(self._commands):
                self._commands[self._currentCommandIndex].setStyleSheet("color: green;")
            self.scrollArea.ensureWidgetVisible(self._commands[self._currentCommandIndex])

        except Exception as e:
            print(f"SliceInfoWidget -> Error displaying the current step : {e}")


    def resetCommandIndex(self):
        """
        resets the current command index to the first one in the list.
        """
        if self._currentCommandIndex < len(self._commands):
            self._commands[self._currentCommandIndex].setStyleSheet("color: black;")
        self._currentCommandIndex = -1

    def show_graph(self):
        self.tabs.ax.clear()

        piece_dict_x:dict[float, List[Position]]= {}
        piece_dict_y:dict[float, List[Position]] = {}

        for piece in self._pieces:
            if not piece in piece_dict_x:
                piece_dict_x[piece] = [piece.position.x]
                piece_dict_y[piece] = [piece.position.y]
            else:
                piece_dict_x[piece].append(piece.position.x)
                piece_dict_y[piece].append(piece.position.y)

        pcb_height = -70.0
        pcb_width = 90.0
        pcb_offset_x = 40.5
        pcb_offset_y = -25.0

        _, _ = plt.subplots()
       # bg = imread("../data/PCB_Background.png")
       # self.tabs.ax.imshow(bg, extent=[pcb_offset_x, pcb_offset_x + pcb_width,
       #                              pcb_offset_y + pcb_height, pcb_offset_y],
       #                 aspect='auto', zorder=0)
        rect = patches.Rectangle((pcb_offset_x,pcb_offset_y), width=pcb_width, height=pcb_height, #TODO Offsets hard-codes
                        linewidth=2, edgecolor = 'black', facecolor='none')
        self.tabs.ax.add_patch(rect)

        #TODO c'est trassh une liste de couleurs de meme 
        colors = ['blue','red','green'] 
        i = 0

        for key in piece_dict_x:
            self.tabs.ax.plot(piece_dict_x[key],piece_dict_y[key],'o', color = colors[i])
            i = i+1

        self.tabs.canvas.draw()
