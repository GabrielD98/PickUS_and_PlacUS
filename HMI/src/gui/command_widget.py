from dataclasses import dataclass
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
    QSlider
)
import utils
from gui.gui_data_manager import GuiDataManager
from gui.button import Button




class CommandWidget(QWidget):

    def __init__(self):
        super().__init__()

        #TODO utiliser des enum de data maybe
        self.on = False 
        self.in_pause = False
        self.data_manager = GuiDataManager()

        layout = QHBoxLayout()
        self.setLayout(layout)
        self.start_button = Button("Start")
        self.pause_button = QPushButton("Pause")

        self.start_button.clicked.connect(self.toggle_start)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setEnabled(False)

        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)


        self.start_button.qss_style.background_color =  "#30E993"
        self.start_button.qss_style.font_size = "25px"
        self.start_button.commitStyleSheet()




    def start(self):
        self.on = True
        self.start_button.setText("Stop")
        self.pause_button.setEnabled(True)
        self.data_manager.start_pnp()




    def stop(self):
        self.on = False
        self.start_button.setText("Start")
        self.pause_button.setEnabled(False)
        self.unpause() #reset le pause button, a voir ak la logique globale TODO
    



    def pause(self):
        self.in_pause = True
        self.pause_button.setText("Continue")
        self.data_manager.pause_pnp()




    def unpause(self):
        self.in_pause = False
        self.pause_button.setText("Pause")
        self.data_manager.continue_pnp()




    def toggle_start(self):
        if self.on: 
            self.stop()
        else:
            self.start()




    def toggle_pause(self):
        if self.in_pause:
            self.unpause()
        else:
            self.pause()