from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import (
    QHBoxLayout, 
	QVBoxLayout,
    QMainWindow, 
    QPushButton,
    QWidget, 
	QLabel,
	QLineEdit, 
	QComboBox,
	QCheckBox,
	QDesktopWidget
)
import json
import utils
from storage import Storage
from data import *
from gui.storage_ui_info import StorageUiInfo
from gui.jog_widget import JogWidget
from controller import Controller


class StorageWindow(QMainWindow):
	"""
	Main window for managing storage calibration and configuration for Pick and Place components.
	Allows users to input, save, and load calibration data, set component states, and configure storage details.

    Attributes:
        _controller (Controller):
            Controller thats allows this object to send commands to the machine
            and receives information from it.
        _storage (Storage):
            instance of the storage data initialise by the user in the calibration phase. 
        _states (dict[StoraheState, str]):
            The different states that the storage can have (for display purposes)
        _piece (Piece):
            The associated with this storage space.
		_pieceName (str):
			The name of the piece to be added.

    """
	def __init__(self, parent=None):
		"""
		Initialize the StorageWindow, set up the UI, and prepare storage controls.
        
		Args:
			parent (QWidget, optional): The parent widget. Defaults to None.
		"""
		super().__init__(parent)
		self.setWindowTitle("Storage Manager")
		
		# main relevant attributes 
		self._storage = Storage()
		self._controller = Controller()
		self._piece:Piece = None
		self._pieceName = "Unknown"
		self._states = {
			"available" : StorageState.USING,
			"ignore this component" : StorageState.IGNORE,
			"storage is empty": StorageState.EMPTY
		}

		# init of global layout and widget
		globalWidget = QWidget()
		globalLayout = QVBoxLayout()
		self.setCentralWidget(globalWidget)
		globalWidget.setLayout(globalLayout)
	
		self._inputsLayout = QVBoxLayout()
		self._inputsLayout.setSpacing(30)


		# section of the button options
		_saveJsonButton = QPushButton("Save Current Calibration")
		_saveJsonButton.clicked.connect(lambda : self._saveCurrentCalibration())
		
		_loadJsonButton = QPushButton("Load Previous Calibration")
		_loadJsonButton.clicked.connect(lambda : self._loadPreviousCalibration())
		
		button = QPushButton("Confirm")
		button.clicked.connect(lambda : self._closeWindow())
		globalLayout.addLayout(self._inputsLayout)

		jsonLayout = QHBoxLayout()
		jsonLayout.setSpacing(30)
		jsonLayout.addWidget(_saveJsonButton)
		jsonLayout.addWidget(_loadJsonButton)

		globalLayout.addLayout(jsonLayout)
		globalLayout.addWidget(button)

		


	def center(self):
		"""
		Calculates the screen center and moves the window there.
		"""
		self.adjustSize() 
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())




	def closeEvent(self, event: QEvent):
		"""
		Override the default close event handler to ensure proper cleanup.
		"""
		self._closeWindow()




	def setInputs(self, info:StorageUiInfo):
		"""
		Set up the input fields for a given storage piece, including quantity, 
		delta, rotation, state, and calibration.
        
		Args:
			info (StorageUiInfo): The storage UI info widget for the piece.
		"""
		if info is None:
			return
		
		utils.clearLayout(self._inputsLayout)
		self._widgetInfo = info
		self._pieceName = info._piece.package
		
		pieceLabel = QLabel(self._pieceName)

		quantityLayout = QHBoxLayout()
		amountLabel = QLabel("Quantity:")
		self._quantityEntry = QLineEdit(self)
		quantityLayout.addWidget(amountLabel)
		quantityLayout.addWidget(self._quantityEntry)

		#init of the entries for the storage delta position between each pieces
		deltaLayout = QHBoxLayout()
		self._deltaLabel = QLabel("Distance between each pieces :")
		self._deltaEntryX = QLineEdit(self)
		self._deltaEntryY = QLineEdit(self)
		self._deltaEntryZ = QLineEdit(self)
		self._deltaEntryYaw = QLineEdit(self)
		self._deltaEntryX.setText("0")
		self._deltaEntryY.setText("0")
		self._deltaEntryZ.setText("0")
		self._deltaEntryYaw.setText("0")
		self._deltaEntryX.setFixedWidth(100)
		self._deltaEntryY.setFixedWidth(100)
		self._deltaEntryZ.setFixedWidth(100)
		self._deltaEntryYaw.setFixedWidth(100)
		deltaLayout.addWidget(self._deltaLabel)
		deltaLayout.addWidget(QLabel("x"))
		deltaLayout.addWidget(self._deltaEntryX)
		deltaLayout.addWidget(QLabel("y"))
		deltaLayout.addWidget(self._deltaEntryY)
		deltaLayout.addWidget(QLabel("z"))
		deltaLayout.addWidget(self._deltaEntryZ)
		deltaLayout.addWidget(QLabel("yaw"))
		deltaLayout.addWidget(self._deltaEntryYaw)


		#init of the rotation options for the storage position
		rotationLayout = QHBoxLayout()
		rotationLabel = QLabel("Component rotation (deg) : ")
		self._rotationOptions = QComboBox(self)
		self._rotationOptions.addItems(["0", "90", "180", "270"])
		rotationLayout.addWidget(rotationLabel)
		rotationLayout.addWidget(self._rotationOptions)

		# init of the different states the storage can have (using, empty, ignore)
		statesLayout = QHBoxLayout()
		statesLabel = QLabel("Component availabilty : ")
		self._statesOptions = QComboBox(self)
		self._statesOptions.addItems(list(self._states.keys()))
		statesLayout.addWidget(statesLabel)
		statesLayout.addWidget(self._statesOptions)

		# checkbox for the automation of the storage
		self._autoCheckbox = QCheckBox("Is the Feeder Automatic")
		self._autoCheckbox.stateChanged.connect(self._onStateChanged)
		
		# section for the manual calibration 
		self._calibrationLayout = QVBoxLayout()
		infoLabel = QLabel("Place the tip of the gripper on the first commponent of the storage")
		self._calibrationLayout.addWidget(infoLabel)
		self._jogWidget = JogWidget(isMain=False)
		self._calibrationLayout.addWidget(self._jogWidget)

		# adds all of the abouve layout in widget in the desired order. 
		self._inputsLayout.addWidget(pieceLabel)
		self._inputsLayout.addLayout(quantityLayout)
		self._inputsLayout.addWidget(self._autoCheckbox)
		self._inputsLayout.addLayout(deltaLayout)
		self._inputsLayout.addLayout(rotationLayout)
		self._inputsLayout.addLayout(statesLayout)
		self._inputsLayout.addLayout(self._calibrationLayout)
		self.center()



	def _saveCurrentCalibration(self):
		"""
		Save the current calibration and configuration for the selected piece to the calibration file.
		Validates input and updates the JSON data structure.
		"""
		
		value = self._quantityEntry.text()
		if not utils.is_int(value):
			print(f"Invalid input for the quantity. Must be an interger, is instead : {value}")
			return
		
		# values to be saved in the JSON 
		automatic = self._autoCheckbox.isChecked()
		state = self._statesOptions.currentIndex()
		rotation = self._rotationOptions.currentIndex()
		deltaPos = Position(0,0,0,0)
		position= self._controller.get_gripper_position()

		if not automatic:
			deltaPos = self._getDeltaPos()

		data = self._readJsonData()	

		if self._pieceName not in data:
			data[self._pieceName] = {}
		if "deltaPos" not in data[self._pieceName]:
			data[self._pieceName]["deltaPos"] = {}

		if "position" not in data[self._pieceName]:
			data[self._pieceName]["position"] = {}


		# saves the entries in a dictionary
		data[self._pieceName]["quantity"] = value
		data[self._pieceName]["automatic"] = automatic
		data[self._pieceName]["state"] = state
		data[self._pieceName]["rotation"] = rotation
		data[self._pieceName]["deltaPos"]["x"] = str(round(deltaPos.x, 2))
		data[self._pieceName]["deltaPos"]["y"] = str(round(deltaPos.y, 2))
		data[self._pieceName]["deltaPos"]["z"] = str(round(deltaPos.z, 2))
		data[self._pieceName]["deltaPos"]["yaw"] = str(round(deltaPos.yaw, 2))
		data[self._pieceName]["position"]["x"] = str(round(position.x, 2))
		data[self._pieceName]["position"]["y"] = str(round(position.y, 2))
		data[self._pieceName]["position"]["z"] = str(round(position.z, 2))
		data[self._pieceName]["position"]["yaw"] = str(round(position.yaw, 2))
		

		with open(CALIB_PATH, "w") as file:
			json.dump(data, file, indent=4)




	def _loadPreviousCalibration(self):
		"""
		Load the previous calibration and configuration for the selected piece from the calibration file.
		Populates the UI fields with the loaded data.
		"""

		data = self._readJsonData()

		key = self._pieceName
		if not key in data:
			return
		
		self._quantityEntry.setText(data[key]["quantity"] )
		self._autoCheckbox.setChecked(bool(data[key]["automatic"]))
		self._statesOptions.setCurrentIndex(data[key]["state"])
		self._rotationOptions.setCurrentIndex(data[key]["rotation"])
		self._deltaEntryX.setText(data[key]["deltaPos"]["x"])
		self._deltaEntryY.setText(data[key]["deltaPos"]["y"])
		self._deltaEntryZ.setText(data[key]["deltaPos"]["z"])
		self._deltaEntryYaw.setText(data[key]["deltaPos"]["yaw"])
		self._jogWidget.x_entry.setText(data[key]["position"]["x"])
		self._jogWidget.y_entry.setText(data[key]["position"]["y"])
		self._jogWidget.z_entry.setText(data[key]["position"]["z"])
		self._jogWidget.yaw_entry.setText(data[key]["position"]["yaw"])




	def _readJsonData(self):
		"""
		Read the calibration data from the calibration JSON file. If the file does not exist or is corrupted,
		it creates a new file with an empty dictionary.
        
		Returns:
			dict: The calibration data.
		"""
		try:
			with open(CALIB_PATH, 'r') as file:
				data = json.load(file)
		except (FileNotFoundError, json.JSONDecodeError):
			# Create the file with an empty dictionary if it's missing or corrupted
			with open(CALIB_PATH, 'w') as file:
				data  = {}
				json.dump(data, file)

		return data


	def _openCalibrationTab(self):
		"""
		Open the calibration tab, clearing the layout and adding calibration instructions and jog widget.
		"""
		utils.clearLayout(self._calibrationLayout)
		info_label = QLabel("Place the tip of the gripper on the first commponent of the storage")
		self._calibrationLayout.addWidget(info_label)
		self._calibrationLayout.addWidget(JogWidget(isMain=False))





	def _onStateChanged(self, state):
		"""
		Handle the state change of the automatic checkbox, enabling or disabling delta input fields.
        
		Args:
			state (int): The state of the checkbox (Qt.Checked or not).
		"""

		enabled = True
		if state == 2: # 2 = Qt.Checked
			enabled = False
		self._deltaLabel.setEnabled(enabled)
		self._deltaEntryX.setEnabled(enabled)
		self._deltaEntryY.setEnabled(enabled)
		self._deltaEntryZ.setEnabled(enabled)
		self._deltaEntryYaw.setEnabled(enabled)		
	



	def _getDeltaPos(self) -> Position:
		"""
		Get the delta position values from the input fields, validating them as floats.
        
		Returns:
			Position: The delta position as a Position object, or None if invalid input.
		"""
		xValue = self._deltaEntryX.text()
		yValue = self._deltaEntryY.text()
		zValue = self._deltaEntryZ.text()
		yawValue = self._deltaEntryYaw.text()

		if not utils.is_float(xValue):
			print(f"Invalid input for the x position delta. Must be a float, is instead : {xValue}")
			return None
		if not utils.is_float(yValue):
			print(f"Invalid input for the y position delta. Must be a float, is instead : {yValue}")
			return None
		if not utils.is_float(zValue):
			print(f"Invalid input for the z position delta. Must be a float, is instead : {zValue}")
			return None
		if not utils.is_float(yawValue):
			print(f"Invalid input for the yaw position delta. Must be a float, is instead : {yawValue}")
			return None

		return Position(float(xValue), float(yValue), float(zValue), float(yawValue))




	def _closeWindow(self):
		"""
		Saves the value of the entries in memory before closing this window. 
		If some entries are invalid, nothing is saved. 
		"""
		value = self._quantityEntry.text()
		if not utils.is_int(value):
			msg = f"Invalid input for the quantity. Must be an interger, is instead : [{value}]"
			print(msg)
			errorWindow = utils.ErrorWindow(error_msg=msg)
			errorWindow.show()
			return
		
		# reads the user inputs 
		quantity = int(value)
		automatic = self._autoCheckbox.isChecked()
		state = self._states[self._statesOptions.currentText()]
		rotation = int(self._rotationOptions.currentText())
		deltaPos = Position(0,0,0,0)
		position = self._controller.get_gripper_position()
		position.yaw = rotation

		if not automatic:
			deltaPos = self._getDeltaPos()
			if deltaPos is None:
				return

		# saves the data acquired
		self._storage.addComponent(self._widgetInfo._piece, position, deltaPos, state, quantity, automatic)
		self._widgetInfo.updateAll(self._pieceName, state, quantity, automatic)
		print("piece added successfully")

		# closes the window
		self.deleteLater()

	