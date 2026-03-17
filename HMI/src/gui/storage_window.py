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
from gui.gui_data_manager import GuiDataManager

class StorageWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Storage Manager")
		self.storage = Storage()
		self.data_manager = GuiDataManager()
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

		delta_layout = QHBoxLayout()
		self.delta_label = QLabel("Distance between each pieces :")
		self.delta_entry_x = QLineEdit(self)
		self.delta_entry_y = QLineEdit(self)
		self.delta_entry_z = QLineEdit(self)
		self.delta_entry_yaw = QLineEdit(self)
		self.delta_entry_x.setText("0")
		self.delta_entry_y.setText("0")
		self.delta_entry_z.setText("0")
		self.delta_entry_yaw.setText("0")
		self.delta_entry_x.setFixedWidth(100)
		self.delta_entry_y.setFixedWidth(100)
		self.delta_entry_z.setFixedWidth(100)
		self.delta_entry_yaw.setFixedWidth(100)
		delta_layout.addWidget(self.delta_label)
		delta_layout.addWidget(QLabel("x"))
		delta_layout.addWidget(self.delta_entry_x)
		delta_layout.addWidget(QLabel("y"))
		delta_layout.addWidget(self.delta_entry_y)
		delta_layout.addWidget(QLabel("z"))
		delta_layout.addWidget(self.delta_entry_z)
		delta_layout.addWidget(QLabel("yaw"))
		delta_layout.addWidget(self.delta_entry_yaw)


		rotation_layout = QHBoxLayout()
		rotation_label = QLabel("Component rotation (deg) : ")
		self.rotation_options = QComboBox(self)
		self.rotation_options.addItems(["0", "90", "180", "270"])
		rotation_layout.addWidget(rotation_label)
		rotation_layout.addWidget(self.rotation_options)

		states_layout = QHBoxLayout()
		states_label = QLabel("Component availabilty : ")
		self.states_options = QComboBox(self)
		self.states_options.addItems(list(self.states.keys()))
		states_layout.addWidget(states_label)
		states_layout.addWidget(self.states_options)

		self.auto_checkbox = QCheckBox("Is the Feeder Automatic")
		self.auto_checkbox.stateChanged.connect(self.on_state_changed)
		
		self.calibration_layout = QVBoxLayout()
		calibrate_button = QPushButton("Calibrate")
		calibrate_button.clicked.connect(self.open_calibration_tab)
		self.calibration_layout.addWidget(calibrate_button)

		self.inputs_layout.addWidget(piece_label)
		self.inputs_layout.addLayout(quantity_layout)
		self.inputs_layout.addWidget(self.auto_checkbox)
		self.inputs_layout.addLayout(delta_layout)
		self.inputs_layout.addLayout(rotation_layout)
		self.inputs_layout.addLayout(states_layout)
		self.inputs_layout.addLayout(self.calibration_layout)




	def open_calibration_tab(self):
		utils.clearLayout(self.calibration_layout)
		info_label = QLabel("Place the tip of the gripper on the first commponent of the storage")
		self.calibration_layout.addWidget(info_label)
		self.calibration_layout.addWidget(JogWidget(isMain=False))




	def closeEvent(self, event: QEvent):
		"""Override the default close event handler."""
		self.close_window()




	def on_state_changed(self, state):

		enabled = True
		if state == 2: # 2 = Qt.Checked
			enabled = False
		self.delta_label.setEnabled(enabled)
		self.delta_entry_x.setEnabled(enabled)
		self.delta_entry_y.setEnabled(enabled)
		self.delta_entry_z.setEnabled(enabled)
		self.delta_entry_yaw.setEnabled(enabled)		
	



	def get_delta_pos(self) -> Position:
		x_value = self.delta_entry_x.text()
		y_value = self.delta_entry_y.text()
		z_value = self.delta_entry_z.text()
		yaw_value = self.delta_entry_yaw.text()

		if not utils.is_float(x_value):
			print(f"Invalid input for the x position delta. Must be a float, is instead : {x_value}")
			return None
		if not utils.is_float(y_value):
			print(f"Invalid input for the y position delta. Must be a float, is instead : {y_value}")
			return None
		if not utils.is_float(z_value):
			print(f"Invalid input for the z position delta. Must be a float, is instead : {z_value}")
			return None
		if not utils.is_float(yaw_value):
			print(f"Invalid input for the yaw position delta. Must be a float, is instead : {yaw_value}")
			return None

		return Position(x_value, y_value, z_value, yaw_value)




	def close_window(self):
		value = self.quantity_entry.text()
		if not utils.is_int(value):
			print(f"Invalid input for the quantity. Must be an interger, is instead : {value}")
			return
		
		quantity = int(value)
		automatic = self.auto_checkbox.isChecked()
		state = self.states[self.states_options.currentText()]
		rotation = int(self.rotation_options.currentText())
		deltaPos = Position(0,0,0,0)
		position= self.data_manager.get_gripper_position()

		if not automatic:
			deltaPos = self.get_delta_pos()
			if deltaPos is None:
				return


		self.storage.addComponent(self.widget_info.piece, position, deltaPos, 
							rotation, state, quantity, automatic)

		self.widget_info.update_all(self.piece_name, state, quantity, automatic)
		print("piece added successfully")
		self.deleteLater()

	