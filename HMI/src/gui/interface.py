from PyQt5.QtCore import QEvent, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QHBoxLayout, 
	QVBoxLayout,
    QMainWindow, 
    QPushButton,
    QWidget, 
    QFileDialog,
    QLineEdit,
	QLabel,
	QScrollArea,
	QMessageBox

)
from PyQt5 import QtWidgets
from pathlib import Path
from controller import Controller
from file_interpreter import FileInterpreter, ReferenceNotFoundError
from gui.pnp_state_widget import PnPStateWidget
from storage import Storage
from data import *
from typing import List
from gui.storage_window import StorageWindow
from gui.storage_ui_info import StorageUiInfo
from gui.jog_widget import JogWidget
from gui.command_widget import CommandWidget
from gui.slice_info_widget import SliceInfoWidget
from gui.calibration_window import CalibrationWindow
from gui.debug_window import DebugWindow
from gui.settings_window import SettingsWindow
from geometry import setWorkspaceLimits
from settings import read_settings
import utils
import random

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

class Interface(QMainWindow):
	"""
	Main application window for PickUS & PlacUS.
	Handles the overall GUI layout, user actions, and coordination between widgets for:

	- File loading and analysis.
	- Storage management and calibration.
	- Slicing and command generation.
	- Machine state monitoring and manual jogging.
	- Image display and periodic updates.

	Attributes:
        _calibrationPos (Position): 
            The position used for the calibration of the PCB position.
		_pieces (List[Piece]):
			List of all the piece to be placed by the PnP. Needed for the slicing logic.
		_filePath (str):
			The displayed path of the open .pos file.
        _controller (Controller):
            Controller thats allows this object to send commands to the machine and receives information from it.
	"""
	def __init__(self):
		super().__init__()	

		# main relevant attributes 
		self._calibrationPos = Position(-1,-1,-1,-1)
		self._controller = Controller()
		self._pieces:List[Piece] = []
		self._filePath = "No file selected"
		self._debugWindow = None
		self._settingsWindow = None

		self._initializeGUI()

	


	def _initializeGUI(self) :
		"""
		Set up the main GUI layout, initialize all widgets, connect signals, and start the update timer.
		"""
		
		self.setWindowTitle("PickUS & PlacUS")
		self.setMinimumSize(800, 600)

		globalWidget = QWidget()
		globalLayout = QHBoxLayout()
		globalWidget.setLayout(globalLayout)
		self._storageWindow:StorageWindow = None

		# global layouts (overall structure of the UI)
		leftLayout = QVBoxLayout()
		rightLayout = QVBoxLayout()
		globalLayout.addLayout(leftLayout, 2)
		globalLayout.addLayout(rightLayout, 1)
		globalLayout.setStretch(0, 2) # Left side
		globalLayout.setStretch(1, 1) # Right side


		#FILE READING LAYOUT
		exploreFile = QPushButton("Open .pos file")
		exploreFile.clicked.connect(self._openFileDialog)
		self._fileLabel = QLineEdit('No File Selected', alignment=Qt.AlignLeft|Qt.AlignVCenter)
		self._fileLabel.setReadOnly(True)
		self._fileLabel.setStyleSheet("color: black; background-color: white")
		self._referenceLabel = QLineEdit("J4", alignment=Qt.AlignLeft|Qt.AlignVCenter)
		self._referenceLabel.setPlaceholderText("Reference")
		
		self._analyseButton = QPushButton("Analyse")
		self._analyseButton.clicked.connect(self._analyseFile)
		self._analyseButton.setEnabled(False)
		fileLayout = QHBoxLayout()
		fileLayout.addWidget(exploreFile, 1)
		fileLayout.addWidget(self._fileLabel, 5)
		fileLayout.addWidget(self._referenceLabel, 1)
		fileLayout.addWidget(self._analyseButton, 1)
		leftLayout.addLayout(fileLayout, 1)


		#STORAGE PIECE LAYOUT
		self._piecesLayout = QVBoxLayout()
		scroll = QScrollArea(self)	
		leftLayout.addWidget(scroll, 4)
		scroll.setWidgetResizable(True)
		self._piecesLayout.setAlignment(Qt.AlignTop)
		scrollContent = QWidget(scroll)
		scrollContent.setLayout(self._piecesLayout)
		scroll.setWidget(scrollContent)


		#CALIBRATION LAYOUT
		self._calibrateButton = QPushButton("Calibrate")
		self._calibrateButton.clicked.connect(lambda : self._startCalibration())
		self._calibrateButton.setEnabled(False)
		calibrationLayout = QHBoxLayout()
		calibrationLayout.addWidget(self._calibrateButton)
		leftLayout.addLayout(calibrationLayout, 4)


		# SLICE LAYOUT
		sliceLayout = QHBoxLayout()
		self._sliceWidget = SliceInfoWidget(self._calibrationPos)
		self._sliceWidget.setMinimumHeight(100) # Allow it to be smaller
		self._sliceWidget.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
		sliceLayout.addWidget(self._sliceWidget)
		leftLayout.addLayout(sliceLayout, 10)

		#COMMAND LAYOUT 
		commandsLayout = QHBoxLayout()
		commandWidget = CommandWidget()
		commandsLayout.addWidget(commandWidget)
		leftLayout.addLayout(commandsLayout, 2)


		#PNP STATE LAYOUT
		stateLayout = QHBoxLayout()
		self._stateWidget = PnPStateWidget()
		stateLayout.addWidget(self._stateWidget)
		rightLayout.addLayout(stateLayout, 1)

		#DEBUG LAYOUT
		debugLayout = QHBoxLayout()
		self._debugButton = QPushButton("Debug")
		self._debugButton.clicked.connect(self._openDebugWindow)
		self._settingsButton = QPushButton("Settings")
		self._settingsButton.clicked.connect(self._openSettingsWindow)
		debugLayout.addWidget(self._debugButton)
		debugLayout.addWidget(self._settingsButton)
		rightLayout.addLayout(debugLayout, 0)


		# JOG AND MANUAL CONTROL LAYOUT
		jogLayout = QHBoxLayout()
		jogLayout.addWidget(JogWidget())
		rightLayout.addLayout(jogLayout, 4)


		# JULIUS IMAGE LAYOUT
		img_label = QLabel(self)
		img = DATA_DIR / "a_joyful_Julius_C.png"
		rand_num = random.randint(1, 20)
		if rand_num == 1:
			img = DATA_DIR / "julius_salad.png"
		pixmap = QPixmap(str(img))
		img_label.setPixmap(pixmap)
		img_label.setScaledContents(True) 
		img_label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
		rightLayout.addWidget(img_label, 4)

		#overall setup of the window
		self.setCentralWidget(globalWidget)
		self.showMaximized()
		self._applySavedSettings()

		# sets up signals to get info when a task is ended
		self._sliceWidget.sliceDoneSignal.connect(commandWidget.sliceDone)
		self._stateWidget.pnpDoneSignal.connect(commandWidget.pnpDone)

		# Set up the update loop
		self.timer = QTimer(self)
		self.timer.setInterval(100) # Update every 100 milliseconds
		self.timer.timeout.connect(self._updateGUI) 
		self.timer.start() 


	def _applySavedSettings(self):
		settings = read_settings()
		if not settings:
			return

		pressure = settings.get("pressure")
		if isinstance(pressure, dict):
			pick = self._coerce_int(pressure.get("pick"), None)
			place = self._coerce_int(pressure.get("place"), None)
			if pick is not None and place is not None:
				self._sliceWidget.setPressureThresholds(pick, place)

		geometry = settings.get("geometry")
		if isinstance(geometry, dict):
			x_min = self._coerce_float(geometry.get("x_min"), None)
			x_max = self._coerce_float(geometry.get("x_max"), None)
			y_min = self._coerce_float(geometry.get("y_min"), None)
			y_max = self._coerce_float(geometry.get("y_max"), None)
			z_min = self._coerce_float(geometry.get("z_min"), None)
			z_max = self._coerce_float(geometry.get("z_max"), None)
			if None not in (x_min, x_max, y_min, y_max, z_min, z_max):
				try:
					setWorkspaceLimits(x_min, x_max, y_min, y_max, z_min, z_max)
				except ValueError:
					pass

		if "parsing_enabled" in settings:
			self._controller.setCommandParsingEnabled(bool(settings.get("parsing_enabled")))


	@staticmethod
	def _coerce_float(value, fallback: float | None):
		try:
			return float(value)
		except (TypeError, ValueError):
			return fallback

	@staticmethod
	def _coerce_int(value, fallback: int | None):
		try:
			return int(value)
		except (TypeError, ValueError):
			return fallback





	def _openFileDialog(self):
		"""
		Open a file dialog for the user to select a .pos file (KiCad position file).
		If a new file is open, resets relevant widgets (file path and analyse button).

		#TODO file manager should be another object to make this class
		tasks more clear and concise.
		"""
		filename, _ = QFileDialog.getOpenFileName(
			parent=self,               
			caption="Select a File",
			directory=str(DATA_DIR), 
			filter="All Files (*.pos)" 
		)

		if not filename:
			return
		
		self._filePath = str(Path(filename))
		self._fileLabel.setText(self._filePath)
		self._analyseButton.setEnabled(True)
		self._analyseButton.setText("Analyse")
		utils.clearLayout(self._piecesLayout)

		self._calibrateButton.setEnabled(False)
		self._sliceWidget.reset()

		


	def _analyseFile(self):
		"""
		Analyse the selected .pos file, extract pieces, 
		update the slice widget and piece list.
		Enable calibration (The user can only calibrate once a file is loaded).
		"""
		referenceRef = self._referenceLabel.text().strip() or "J4"
		try:
			pieces = FileInterpreter().readPositionFile(self._filePath, referenceRef)
		except ReferenceNotFoundError:
			QMessageBox.critical(
				self,
				"Reference not found",
				f"The reference '{referenceRef}' was not found in the .pos file. Please update it and analyse again."
			)
			self._analyseButton.setEnabled(True)
			self._analyseButton.setText("Analyse")
			self._calibrateButton.setEnabled(False)
			return
		if pieces is None:
			return
		
		self._sliceWidget.setPieces(pieces)
		self._pieces = self._getAllUniquePiece(pieces)
		self._updatePieceList()
		self._analyseButton.setEnabled(False)
		self._calibrateButton.setEnabled(True)
		self._analyseButton.setText("Analysis Completed")




	def _getAllUniquePiece(self, pieces:List[Piece]) -> List[Piece]:
		"""
		Return a list of unique Piece objects from the provided list.
        
		Args:
			pieces (List[Piece]): List of Piece objects (may contain duplicates).
		Returns:
			List[Piece]: List of unique Piece objects.
		"""
		uniquePieces:dict[Piece:Piece] = {}
		for piece in pieces:
			if piece not in uniquePieces:
				uniquePieces[piece] = piece
		return list(uniquePieces.values())
    



	def _updatePieceList(self):
		"""
		Populate the GUI with widgets for each unique piece, allowing the user to add them to storage.
		"""
		for piece in self._pieces:
			layout = QHBoxLayout()
			button = QPushButton("Add to Storage")
			storageInfo = StorageUiInfo(piece, button)

			# lambda should have this form to keep data in memory
			button.clicked.connect(lambda _, info=storageInfo: 
						  self._addPieceToStorage(info))
			
			layout.addWidget(storageInfo, 4)
			layout.addWidget(button, 1)
			self._piecesLayout.addLayout(layout)
		self._piecesLayout.addStretch(1)




	def _addPieceToStorage(self, info:StorageUiInfo):
		"""
		Open the storage window for the selected piece, allowing the user to configure and add it to storage.
        
		Args:
			info (StorageUiInfo): The storage UI info widget for the piece.
		"""
		self._storageWindow = StorageWindow()
		self._storageWindow.setInputs(info)
		self._storageWindow.show()




	def _startCalibration(self):
		"""
		Open the calibration window to configure the position of the PCB.
		Then enables slicing.
		"""
		self._calibrationWindow = CalibrationWindow(position=self._calibrationPos)
		self._calibrationWindow.show()
		self._sliceWidget.enableSlicing()

	def _openDebugWindow(self):
		"""Open the debug window for comm logs and manual controls."""
		if self._debugWindow is None or not self._debugWindow.isVisible():
			self._debugWindow = DebugWindow(self._controller)
			self._debugWindow.show()
		else:
			self._debugWindow.raise_()
			self._debugWindow.activateWindow()

	def _openSettingsWindow(self):
		"""Open the settings window for pressure and geometry."""
		if self._settingsWindow is None or not self._settingsWindow.isVisible():
			self._settingsWindow = SettingsWindow(self._sliceWidget)
			self._settingsWindow.show()
		else:
			self._settingsWindow.raise_()
			self._settingsWindow.activateWindow()




	def _updateGUI(self):
		"""
		Periodically update the GUI based on the controller's connection and state.
		Displays the machine state via the stateWidget listener. 
		Runs every 100ms via a QTimer.
		"""
		if not self._controller.isConnected():
			if not self._controller.isPortOpen():
				self._stateWidget.updateScannedPort()
			#TODO check for disconnection with exeption request. connected should not be local here
			else :	
				self._stateWidget.setDisconnected()		
		else :
			self._stateWidget.updateState()



	
	def closeEvent(self, _: QEvent):
		"""
		Override the default close event handler to stop the timer and disconnect from the machine.
		"""
		if self.timer.isActive():
			self.timer.stop()
		self.deleteLater()	
		self._controller.disconnectionFromMachine()