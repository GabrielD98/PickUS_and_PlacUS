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
	QScrollArea
)
from PyQt5 import QtWidgets
from pathlib import Path
from controller import Controller
from file_interpreter import FileInterpreter
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
from gui.frame import Frame,WidgetConfig
from gui.button import Button
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

		self._initializeGUI()

	


	def _initializeGUI(self) :
		"""
		Set up the main GUI layout, initialize all widgets, connect signals, and start the update timer.
		"""
		
		self.setWindowTitle("PickUS & PlacUS")
		self.setMinimumSize(800, 600)

		globalWidget = QWidget()
		# globalWidget.setStyleSheet("border-image: url('../data/Marble_Background.png') 100 100 100 100 stretch; background-repeat: no-repeat;" 
       	#	"background-position: center; border: none;")

		globalLayout = QHBoxLayout()
		globalWidget.setLayout(globalLayout)
		self._storageWindow:StorageWindow = None

		#Global background 
		# 2. Set the object name to avoid inheritance issues
		globalWidget.setObjectName("MainBackground")

		# 3. Apply the stylesheet with a clean string
		# Note: Ensure there are no curly braces {} inside the string other than the CSS blocks
		globalWidget.setStyleSheet(f"""
			QWidget#MainBackground {{
				border-image: url('../data/Marble_Background.png') 100 100 100 100 stretch stretch;
				background-repeat: no-repeat;
				background-position: center;
			}}
		""")

		globalWidget.setAttribute(Qt.WA_StyledBackground, True)

		# global layouts (overall structure of the UI)
		leftLayout = QVBoxLayout()
		rightLayout = QVBoxLayout()
		globalLayout.addLayout(leftLayout, 2)
		globalLayout.addLayout(rightLayout, 1)
		globalLayout.setStretch(0, 2) # Left side
		globalLayout.setStretch(1, 1) # Right side


		#FILE READING LAYOUT
		exploreFile = Button("Open .pos file")
		exploreFile.qss_style.image_path = '../data/Light_Bronze_Button.png'
		exploreFile.qss_style.hover_image_path = '../data/Short_Hover_Button.png'
		exploreFile.commitStyleSheet()

		exploreFile.clicked.connect(self._openFileDialog)
		self._fileLabel = QLineEdit('No File Selected', alignment=Qt.AlignLeft|Qt.AlignVCenter)
		self._fileLabel.setReadOnly(True)
		self._fileLabel.setStyleSheet("color: black; background-color: white")
		
		self._analyseButton = Button("Analyse")
		self._analyseButton.qss_style.image_path = '../data/Light_Bronze_Button.png'
		self._analyseButton.qss_style.hover_image_path = '../data/Short_Hover_Button.png'
		self._analyseButton.commitStyleSheet()


		self._analyseButton.clicked.connect(self._analyseFile)
		self._analyseButton.setEnabled(False)
		fileLayout = QHBoxLayout()
		fileLayout.addWidget(exploreFile, 1)
		fileLayout.addWidget(self._fileLabel, 5)
		fileLayout.addWidget(self._analyseButton, 1)
		leftLayout.addLayout(fileLayout, 1)


		#STORAGE PIECE LAYOUT
		self._piecesLayout = QVBoxLayout()
		scroll = QScrollArea(self)	
		scroll.setWidgetResizable(True)

		scroll.setStyleSheet("background: transparent; border: none;")
		scroll.viewport().setStyleSheet("background: transparent;")
		
		self._piecesLayout.setAlignment(Qt.AlignTop)
		scrollContent = QWidget()
		scrollContent.setStyleSheet("background: transparent;")
		scrollContent.setLayout(self._piecesLayout)
		scroll.setWidget(scrollContent)

		self.framed_scroll = Frame(scroll, style=WidgetConfig(
			image_path = "../data/Storage_Background_VF.png",
			slices = "100 100 100 100",
            background_color="transparent"
        ))

		leftLayout.addWidget(self.framed_scroll,4)

		#CALIBRATION LAYOUT
		self._calibrateButton = Button("Calibrate")
		self._calibrateButton.qss_style.font_size = "22px"
		self._calibrateButton.qss_style.image_path = '../data/Long_Light_Bronze_Button.png'
		self._calibrateButton.qss_style.slices = "0 0 0 0"
		self._calibrateButton.qss_style.hover_image_path = '../data/Long_Bronze_Hovered_Button.png'
		self._calibrateButton.qss_style.slices_hover = "0 0 0 0"
		self._calibrateButton.commitStyleSheet()

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


		# JOG AND MANUAL CONTROL LAYOUT
		jogLayout = QHBoxLayout()
		jogLayout.addWidget(JogWidget())
		rightLayout.addLayout(jogLayout, 4)


		# JULIUS IMAGE LAYOUT
		img_label = QLabel(self)
		img = DATA_DIR / "Framed_Jules.png"
		rand_num = random.randint(1, 20)
		if rand_num == 1:
			img = DATA_DIR / "Framed_Jules_Salade.png"
		pixmap = QPixmap(str(img))
		img_label.setPixmap(pixmap)
		img_label.setScaledContents(True) 
		img_label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
		rightLayout.addWidget(img_label, 4)

		#overall setup of the window
		self.setCentralWidget(globalWidget)
		self.showMaximized()

		# sets up signals to get info when a task is ended
		self._sliceWidget.sliceDoneSignal.connect(commandWidget.sliceDone)
		self._stateWidget.pnpDoneSignal.connect(commandWidget.pnpDone)
		commandWidget.pnpStartingSignal.connect(self._sliceWidget.resetCommandIndex)
		# cant use pyqtsignals on non pyqt object (controller)
		self._controller.registerCallback(self._sliceWidget.onNextCommand) 

		# Set up the update loop
		self.timer = QTimer(self)
		self.timer.setInterval(100) # Update every 100 milliseconds
		self.timer.timeout.connect(self._updateGUI) 
		self.timer.start() 





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
		pieces = FileInterpreter().readPositionFile(self._filePath)
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
			button = Button("Add to Storage")
			button.qss_style.hover_image_path = '../data/Short_Hover_Button.png'
			button.commitStyleSheet()
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