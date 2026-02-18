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
from gui.storage_ui_info import StorageUiInfo
from gui.jog_widget import JogWidget

class StorageWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Storage Manager")
		self.storage = Storage()
		self.piece:Piece = None
		self.addition_label:QLabel = None
		self.piece_name = "Unknown"
		self.states = {
			"available" : StorageState.USING,
			"ignore this component" : StorageState.IGNORE,
			"storage is empty": StorageState.EMPTY
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
		



	def set_inputs(self, info:StorageUiInfo):
		if info is None:
			return
		
		utils.clearLayout(self.inputs_layout)
		self.widget_info = info
		self.piece_name = info.piece.package
		
		piece_label = QLabel(self.piece_name)

		quantity_layout = QHBoxLayout()
		amount_label = QLabel("Quantity:")
		self.quantity_entry = QLineEdit(self)
		quantity_layout.addWidget(amount_label)
		quantity_layout.addWidget(self.quantity_entry)


		self.states_options = QComboBox(self)
		self.states_options.addItems(list(self.states.keys()))

		self.auto_checkbox = QCheckBox("Is the Feeder Automatic")
		
		self.calibration_layout = QVBoxLayout()
		calibrate_button = QPushButton("Calibrate")
		calibrate_button.clicked.connect(self.open_calibration_tab)
		self.calibration_layout.addWidget(calibrate_button)

		self.inputs_layout.addWidget(piece_label)
		self.inputs_layout.addLayout(quantity_layout)
		self.inputs_layout.addWidget(self.states_options)
		self.inputs_layout.addWidget(self.auto_checkbox)
		self.inputs_layout.addLayout(self.calibration_layout)

		

	def open_calibration_tab(self):
		utils.clearLayout(self.calibration_layout)
		info_label = QLabel("Place the tip of the gripper on the first commponent of the storage")
		self.calibration_layout.addWidget(info_label)
		self.calibration_layout.addWidget(JogWidget(isMain=False))


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
		deltaPos = Position(0,0,0,0) #TODO demander la position courante au controleur

		self.storage.addComponent(self.widget_info.piece, deltaPos, state, quantity, automatic)

		self.widget_info.update_all(self.piece_name, state, quantity, automatic)
		print("piece added successfully")
		self.deleteLater()

	