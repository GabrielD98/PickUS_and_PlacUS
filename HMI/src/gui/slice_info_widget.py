import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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

class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Scroll bar")
        self.tabs.addTab(self.tab2, "Graphic")

        self.tab1.layout = QVBoxLayout(self.tab1)
        scroll = QScrollArea(self)
        self.tab1.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        scroll.setWidget(scrollContent)

        self.tab2.layout = QVBoxLayout(self.tab2)
        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.tab2.layout.addWidget(self.canvas)

        self.layout.addWidget(self.tabs)
   

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

        fig, ax = plt.subplots()
        rect = patches.Rectangle((46,-43), width=74, height=-42,
                         linewidth=2, edgecolor = 'black', facecolor='none')
        self.tabs.ax.add_patch(rect)

        #TODO c'est trassh une liste de couleurs de meme 
        colors = ['blue','red','green'] 
        i = 0

        for key in piece_dict_x:
            self.tabs.ax.plot(piece_dict_x[key],piece_dict_y[key],'o', color = colors[i])
            i = i+1

        self.tabs.ax.set_xlim(40, 140)
        self.tabs.ax.set_ylim(-100, -30)

        self.tabs.canvas.draw()