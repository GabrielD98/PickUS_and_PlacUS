import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.image import imread
import time
from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
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
    QScrollArea,
    QTabWidget
)

import utils
from data import Command, Piece, Position
from slicer import Slicer
from storage import Storage
from gui.gui_data_manager import GuiDataManager
from gui.Tab_widget import MyTabWidget

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

        self.tabs = MyTabWidget(self)
        layout.addWidget(self.tabs)

        self.index = 0

       

    def slice(self):
        
        commands = self.slicer.slice(self.pieces,
                                          self.calibration_pos,    #TODO calbiration pos of PCB
                                          Position(0,0,0,0),   #TODO offset du z
                                          50)
        
        self.dataManager.set_pnp_commands(commands)
        utils.clearLayout(self.tabs.scrollLayout)
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
            self.tabs.scrollLayout.addWidget(comLabel)

        self.show_graph()

    def highlight_step(self):
        #TODO initialiser index a 0 in start
        if self.index >= 1:
             self.tabs.scrollLayout.itemAt(self.index - 1).widget().setStyleSheet("background-color: white; color: black")
        self.tabs.scrollLayout.itemAt(self.index).widget().setStyleSheet("background-color: green; color: black") 
        self.index ++ 1 

    def set_pieces(self, pieces:List[Piece]):
        self.pieces = pieces


    def enable_slicing(self):
        self.slice_button.setEnabled(True)

    def reset(self):
        utils.clearLayout(self.tabs.scrollLayout)
        self.slice_button.setEnabled(False)


    def show_graph(self):
        self.tabs.ax.clear()

        piece_dict_x:dict[float] = {}
        piece_dict_y:dict[float] = {}

        for piece in self.pieces:
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

        fig, ax = plt.subplots()
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