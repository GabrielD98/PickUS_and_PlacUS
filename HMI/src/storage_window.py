from PyQt5.QtCore import QSize, Qt,  QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout, 
	QVBoxLayout,
    QMainWindow, 
    QPushButton,
    QWidget, 
	QLabel,
	QFrame,
	QLineEdit, 
	QInputDialog,
	QComboBox,
	QCheckBox
)


from storage import Storage
from data import *
from typing import List
import utils


class StorageWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Storage Manager")
		self.storage = Storage()
		self.piece:Piece = None
		self.addition_label:QLabel = None
		self.piece_name = "Unknown"
		self.states = {
			"available" : 0,
			"ignore this component" : 1,
			"storage is empty": 2
		}

		global_widget = QWidget()
		global_layout = QVBoxLayout()
		self.setCentralWidget(global_widget)
		global_widget.setLayout(global_layout)

		self.inputs_layout = QVBoxLayout()
		self.inputs_layout.setSpacing(50)
		button = QPushButton("Confirm")
		button.clicked.connect(lambda : self.close_window())
		global_layout.addLayout(self.inputs_layout)
		global_layout.addWidget(button)
		



	def set_inputs(self, piece:Piece, addition_label:QLabel):
		if piece is None or addition_label is None:
			return
		
		utils.clearLayout(self.inputs_layout)
		self.piece = piece
		self.piece_name = piece.package

		self.addition_label = addition_label
		
		piece_label = QLabel(self.piece_name)

		quantity_layout = QHBoxLayout()
		amount_label = QLabel("Quantity:")
		self.quantity_entry = QLineEdit(self)
		quantity_layout.addWidget(amount_label)
		quantity_layout.addWidget(self.quantity_entry)


		self.states_options = QComboBox(self)
		self.states_options.addItems(list(self.states.keys()))

		self.auto_checkbox = QCheckBox("Is the Feeder Automatic")

		self.inputs_layout.addWidget(piece_label)
		self.inputs_layout.addLayout(quantity_layout)
		self.inputs_layout.addWidget(self.states_options)
		self.inputs_layout.addWidget(self.auto_checkbox)

	


	def closeEvent(self, event: QEvent):
		"""Override the default close event handler."""
		self.close_window()




	def close_window(self):
		value = self.quantity_entry.text()
		if not utils.is_int(value):
			print(f"Invalid input for the quantity. Must be an interger, is instead : {value}")
			return
		
		quantity = int(value)
		automatic = self.auto_checkbox.isChecked()
		state = self.states[self.states_options.currentText()]
		deltaPos = Position(0,0,0,0) #TODO dealer ak ca dans la calib

		self.storage.addComponent(self.piece, deltaPos, state, quantity, automatic)


		if self.addition_label is not None:
			self.addition_label.setText("(Added)")
			self.addition_label.setStyleSheet("color: green;") 
		print("piece added successfully")
		self.deleteLater()

	