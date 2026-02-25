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
from controller import Controller
from slicer import Slicer
from storage import Storage


class SliceInfoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.slicer = Slicer()
        self.storage = Storage()
        self.commands:List[Command] = []
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
        #for item in items:
        #    self.scrollLayout.addWidget(item)
        scroll.setWidget(scrollContent)




    def slice(self):
        
        self.commands = self.slicer.slice(self.pieces,
                                          Position(0,0,0,0),    #TODO calbiration pos of PCB
                                          Position(0,0,-1,0),   #TODO offset du z
                                          1)
        
        print(self.pieces)
        for command in self.commands:
            position = command.position

            commandInfo = f"Command : {command.commandId} | " 
            piece_info = ""
            if command.piece is not None:
                piece_info = f"Piece : {command.piece.package} | "
            position_info = ""
            if command.piece is not None:
                position_info = f"Position : {position.x}  {position.x}  {position.x}  {position.x} | "
            speed_info = f"Speed : {command.velocity}"


            comLabel = QLabel(commandInfo+piece_info+position_info+speed_info)
            self.scrollLayout.addWidget(comLabel)


    def set_pieces(self, pieces:List[Piece]):
        self.pieces = pieces
        self.slice_button.setEnabled(True)