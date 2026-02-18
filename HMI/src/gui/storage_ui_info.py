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
    QStackedWidget
)

from data import *
from utils import clearLayout

class StorageUiInfo(QWidget):
    def __init__(self, piece:Piece, button:QPushButton):
        super().__init__()
        self.states = {
            StorageState.EMPTY : "EMPTY",
            StorageState.IGNORE : "IGNORE",
            StorageState.USING : "USING"
        }


        #Layout for the storage info
        self.piece = piece
        self.button = button
        self.added:bool = False
        self.stacked_widget = QStackedWidget()

        self.name:str = piece.package
        self.quantity:int = -1
        self.name_label = QLabel(self.name)
        self.state_label = QLabel("state : -")
        self.quantity_label = QLabel("quantity : -")
        self.automatic_label = QLabel("automatic : -")


        self.active_widget = QWidget()
        self.active_layout = QHBoxLayout()
        self.active_layout.setSpacing(30)
        self.active_layout.addWidget(self.name_label)
        self.active_layout.addWidget(self.state_label)
        self.active_layout.addWidget(self.quantity_label)
        self.active_layout.addWidget(self.automatic_label)
        self.active_widget.setLayout(self.active_layout)


        #Layout when the piece is not added yet 
        self.inactive_widget = QWidget()
        self.inactive_layout = QHBoxLayout()
        addition_label = QLabel("(Not Added)")
        addition_label.setStyleSheet("color: red;") 
        self.inactive_widget.setLayout(self.inactive_layout)

        self.inactive_layout.addWidget(QLabel(self.name), 4)
        self.inactive_layout.addWidget(addition_label, 4)

        self.stacked_widget.addWidget(self.inactive_widget)
        self.stacked_widget.addWidget(self.active_widget)
        layout = QHBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        #self.setLayout(self.inactive_layout)




    def update_all(self, name:str, state:StorageState, quantity:int, auto:bool):
        self.update_name(name)
        self.update_state(state)
        self.update_quantity(quantity)
        self.update_automatic_state(auto)
        self.stacked_widget.setCurrentIndex(1)
        self.button.setText("Change")




    def update_name(self, new_name:str):
        self.name = new_name
        self.name_label.setText(self.name)




    def update_state(self, new_state:StorageState):
        self.state_label.setText("state : " + self.states[new_state])




    def update_quantity(self, new_quantity:int):
        self.quantity = new_quantity
        self.quantity_label.setText(f"quantity : {self.quantity}")




    def update_automatic_state(self, new_auto_state:bool):
        new_text = "automatic : False"
        if new_auto_state == True:
            new_text = "automatic : True"
        self.automatic_label.setText(new_text)



