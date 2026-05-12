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
from command_interface import (
    MoveCommand,
    PickCommand,
    PlaceCommand,
    HomeCommand,
    PauseCommand,
    StopCommand,
)

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
        _pieces (List[Piece]):
            list of all the piece to be placed by the PnP. Needed for the slicing logic.
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
        
        #global layout of this widget
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        #actionnable widget
        self._sliceButton = QPushButton("Slice")
        self._sliceButton.clicked.connect(self.slice)
        self._sliceButton.setEnabled(False)
        layout.addWidget(self._sliceButton)

        #Area that displays all of the steps of the slicing
        scroll = QScrollArea(self)
        layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        scroll.setWidget(scrollContent)




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
        utils.clearLayout(self.scrollLayout)

        #displays all of the generated steps in the scroll layout
        for command in commands:
            # determine type and relevant fields
            if isinstance(command, MoveCommand):
                cmd_name = 'MOVE'
                position = command.position
                speedInfo = f"Speed : {command.velocity}"
                pieceInfo = ''
            elif isinstance(command, PickCommand):
                cmd_name = 'PICK'
                position = getattr(command, 'position', Position(0, 0, 0, 0))
                speedInfo = ''
                pieceInfo = ''
            elif isinstance(command, PlaceCommand):
                cmd_name = 'PLACE'
                position = getattr(command, 'position', Position(0, 0, 0, 0))
                speedInfo = ''
                pieceInfo = f"Piece : {command.piece.package} | " if command.piece is not None else ''
            elif isinstance(command, HomeCommand):
                cmd_name = 'HOME'
                position = Position(0, 0, 0, 0)
                speedInfo = ''
                pieceInfo = ''
            elif isinstance(command, PauseCommand):
                cmd_name = 'PAUSE'
                position = Position(0, 0, 0, 0)
                speedInfo = ''
                pieceInfo = ''
            elif isinstance(command, StopCommand):
                cmd_name = 'STOP'
                position = Position(0, 0, 0, 0)
                speedInfo = ''
                pieceInfo = ''
            else:
                cmd_name = type(command).__name__
                position = getattr(command, 'position', Position(0, 0, 0, 0))
                speedInfo = f"Speed : {getattr(command, 'velocity', '')}"
                pieceInfo = f"Piece : {command.piece.package} | " if getattr(command, 'piece', None) is not None else ''

            positionInfo = f"Position : {round(position.x, 2)} {round(position.y, 2)} {round(position.z, 2)} {round(position.yaw, 2)} | " if position is not None else ''

            commandInfo = f"Command : {cmd_name} | "
            comLabel = QLabel(commandInfo + pieceInfo + positionInfo + speedInfo)
            self.scrollLayout.addWidget(comLabel)

        #tells the command widget that the slicing is done
        self.sliceDoneSignal.emit(True)




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
        utils.clearLayout(self.scrollLayout)
        self._sliceButton.setEnabled(False)

