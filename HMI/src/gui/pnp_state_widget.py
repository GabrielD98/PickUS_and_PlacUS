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
from data import Position
from controller import Controller



class PnPStateWidget(QWidget):

    def __init__(self, controller:Controller = None):
        super().__init__()

        layout = QVBoxLayout()
        self.controller = controller
        self.state_label = QLabel("State : -")
        self.state_label.setAlignment(Qt.AlignCenter) 
        self.position = Position(0,0,0,0)
        self.position_label = QLabel(f"Position : {self.position.x}, {self.position.y},"
                                     + f" {self.position.z}, {self.position.yaw}")
        self.position_label.setAlignment(Qt.AlignCenter) 
        

        layout.addWidget(self.state_label)
        layout.addWidget(self.position_label)
        self.setLayout(layout)
        

    def update_state(self):
        state = self.controller.getState()
        self.state_label.setText(f"State : {state[1]}")
        self.position = state[2]
        self.position_label = QLabel(f"Position : {self.position.x}, {self.position.y},"
                                     + f" {self.position.z}, {self.position.yaw}")
