import matplotlib.pyplot as plt
import numpy as np
import time
from typing import List
from PyQt5.QtCore import Qt
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
                                          50)
        
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
                position_info = f"Position : {position.x}  {position.y}  {position.z}  {position.yaw} | "
            speed_info = f"Speed : {command.velocity}"


            comLabel = QLabel(commandInfo+piece_info+position_info+speed_info)
            self.scrollLayout.addWidget(comLabel)

            self.show_graph()


    def set_pieces(self, pieces:List[Piece]):
        self.pieces = pieces


    def enable_slicing(self):
        self.slice_button.setEnabled(True)

    def reset(self):
        utils.clearLayout(self.scrollLayout)
        self.slice_button.setEnabled(False)


    def show_graph(self):

        piece_dict_x:dict[float] = {}
        piece_dict_y:dict[float] = {}

        for piece in self.pieces:
            if not piece in piece_dict_x:
                piece_dict_x[piece] = [piece.position.x]
                piece_dict_y[piece] = [piece.position.y]
            else:
                piece_dict_x[piece].append(piece.position.x)
                piece_dict_y[piece].append(piece.position.y)

        fig, ax = plt.subplots()
        #TODO c'est trassh une liste de couleurs de meme 
        colors = ['blue','red','green']
        i = 0

        for key in piece_dict_x:
            ax.plot(piece_dict_x[key],piece_dict_y[key],'o', color = colors[i])
            i = i+1

        plt.show()