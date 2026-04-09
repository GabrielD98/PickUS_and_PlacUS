import time
from typing import List
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout, 
	QVBoxLayout,
    QMainWindow, 
    QPushButton,
    QWidget, 
    QFileDialog,
    QLineEdit,
	QLabel,
	QFrame,
	QPlainTextEdit,
	QInputDialog,
    QStackedWidget,
    QSlider,
    QScrollArea
)

import utils
from data import Command, Piece, Position
from slicer import Slicer
from storage import Storage
from gui.gui_data_manager import GuiDataManager

class SliceInfoWidget(QWidget):
    slice_done_signal = pyqtSignal(bool) 
    
    def __init__(self, calibration_pos:Position):
        super().__init__()
        self.slicer = Slicer()
        self.calibration_pos = calibration_pos
        self.dataManager = GuiDataManager()
        self.storage = Storage()
        self.pieces:List[Piece] = None


        layout = QVBoxLayout()
        self.setLayout(layout)

        self.slice_button = QPushButton("Slice")
        self.slice_button.clicked.connect(self.slice)
        self.slice_button.setEnabled(False)
        layout.addWidget(self.slice_button)


        scroll = QScrollArea(self)
        layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        scroll.setWidget(scrollContent)




    def slice(self):
        
        commands = self.slicer.slice(self.pieces,
                                          self.calibration_pos,    #TODO calbiration pos of PCB
                                          Position(0,0,0,0),   #TODO offset du z
                                          150)              #TODO wtf is this
        
        self.dataManager.set_pnp_commands(commands)
        utils.clearLayout(self.scrollLayout)
        for command in commands:
            position = command.position

            commandInfo = f"Command : {command.commandId} | " 
            piece_info = ""
            if command.piece is not None:
                piece_info = f"Piece : {command.piece.package} | "
            position_info = ""
            if command.piece is not None:
                position_info = (f"Position : {round(position.x, 2)}" 
                f"{round(position.y, 2)}  {round(position.z, 2)}  {round(position.yaw, 2)} | ")
            speed_info = f"Speed : {command.velocity}"


            comLabel = QLabel(commandInfo+piece_info+position_info+speed_info)
            self.scrollLayout.addWidget(comLabel)
            self.slice_done_signal.emit(True)


    def set_pieces(self, pieces:List[Piece]):
        self.pieces = pieces


    def enable_slicing(self):
        self.slice_button.setEnabled(True)

    def reset(self):
        utils.clearLayout(self.scrollLayout)
        self.slice_button.setEnabled(False)

