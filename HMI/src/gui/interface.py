from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
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
	QInputDialog
)
from PyQt5 import QtWidgets
from pathlib import Path

from controller import Controller
from file_interpreter import FileInterpreter
from gui.pnp_state_widget import PnPStateWidget
from slicer import Slicer
from storage import Storage
from data import *
from typing import List
from gui.storage_window import StorageWindow
from gui.storage_ui_info import StorageUiInfo
from gui.jog_widget import JogWidget
from gui.command_widget import CommandWidget
from gui.slice_info_widget import SliceInfoWidget
from gui.calbration_window import CalibrationWindow
import utils
		



class Interface(QMainWindow):
	def __init__(self):
		super().__init__()	
		self.calibration_pos = Position(-1,-1,-1,-1)
		self.storage_window:StorageWindow = None
		self.controller = Controller()  #TODO controller as a singleton for less crust ?
		self.storage = Storage()
		self.pieces:List[Piece] = []
		self.file_path = "No file selected"
		self.initialize_gui()

	

	def initialize_gui(self) :
		
		self.setWindowTitle("PickUS & PlacUS")


		#testting
		global_widget = QWidget()
		global_layout = QHBoxLayout()
		global_widget.setLayout(global_layout)


		#layouts
		left_layout = QVBoxLayout()
		right_layout = QVBoxLayout()
		global_layout.addLayout(left_layout, 2)
		global_layout.addLayout(right_layout, 1)




		#FILE READING LAYOUT
		explore_file = QPushButton("Open .pos file")
		explore_file.clicked.connect(self.open_file_dialog)
		self.file_label = QLabel('No File Selected', alignment=Qt.AlignLeft|Qt.AlignVCenter)
		self.file_label.setStyleSheet("color: black; background-color: white")
		self.analyse_button = QPushButton("Analyse")
		self.analyse_button.clicked.connect(self.analyse_file)
		self.analyse_button.setEnabled(False)
		file_layout = QHBoxLayout()
		file_layout.addWidget(explore_file, 1)
		file_layout.addWidget(self.file_label, 5)
		file_layout.addWidget(self.analyse_button, 1)
		left_layout.addLayout(file_layout, 1)


		#FILE READING LAYOUT
		self.pieces_layout = QVBoxLayout()
		left_layout.addLayout(self.pieces_layout, 3)

		#TODO delete label
		self.calibrate_button = QPushButton("Calibrate")
		self.calibrate_button.clicked.connect(lambda : self.start_calibration())
		self.calibrate_button.setEnabled(False)
		calibration_layout = QHBoxLayout()
		calibration_layout.addWidget(self.calibrate_button)
		left_layout.addLayout(calibration_layout, 2)


		slice_layout = QHBoxLayout()
		self.slice_widget = SliceInfoWidget()
		slice_layout.addWidget(self.slice_widget)
		left_layout.addLayout(slice_layout)


		commands_layout = QHBoxLayout()
		commands_layout.addWidget(CommandWidget())
		left_layout.addLayout(commands_layout, 2)


		state_layout = QHBoxLayout()
		state_layout.addWidget(PnPStateWidget(self.controller))
		right_layout.addLayout(state_layout, 1)


		jog_layout = QHBoxLayout()
		jog_layout.addWidget(JogWidget(controller=self.controller))
		right_layout.addLayout(jog_layout, 4)


		img_label = QLabel(self)
		pixmap = QPixmap("../data/a_joyful_Julius_C.png")
		img_label.setPixmap(pixmap)
		right_layout.addWidget(img_label, 4)

		
		self.setCentralWidget(global_widget)
		self.showMaximized()





	def open_file_dialog(self):
		filename, _ = QFileDialog.getOpenFileName(
			parent=self,               
			caption="Select a File",
			directory="../data/", 
			filter="All Files (*.pos)" 
		)

		if not filename:
			return

		self.file_path = str(Path(filename))
		self.file_label.setText(self.file_path)
		self.analyse_button.setEnabled(True)
		self.analyse_button.setText("Analyse")
		utils.clearLayout(self.pieces_layout)

		self.calibrate_button.setEnabled(False)
		self.slice_widget.reset()

		


	def analyse_file(self):
		pieces = FileInterpreter().readPositionFile(self.file_path)
		if pieces is None:
			return
		
		self.slice_widget.set_pieces(pieces)
		self.pieces = self.get_all_unique_piece(pieces)
		self.update_piece_list()
		self.analyse_button.setEnabled(False)
		self.calibrate_button.setEnabled(True)
		self.analyse_button.setText("Analysis Completed")





	def get_all_unique_piece(self, pieces:List[Piece]) -> List[Piece]:
		unique_pieces:dict[Piece:Piece] = {}
		for piece in pieces:
			if piece not in unique_pieces:
				unique_pieces[piece] = piece
		return list(unique_pieces.values())
    


	def update_piece_list(self):


		for piece in self.pieces:
			layout = QHBoxLayout()
			button = QPushButton("Add to Storage")
			storage_info = StorageUiInfo(piece, button)
			button.clicked.connect(lambda _, info=storage_info: 
						  self.add_piece_to_storage(info))

			layout.addWidget(storage_info, 4)
			layout.addWidget(button, 1)
			self.pieces_layout.addLayout(layout)




	def add_piece_to_storage(self, info:StorageUiInfo):
		self.storage_window = StorageWindow(controller=self.controller)
		self.storage_window.set_inputs(info)
		self.storage_window.show()


	def start_calibration(self):
		self.calibration_window = CalibrationWindow(position=self.calibration_pos, controller=self.controller)
		self.calibration_window.show()
		self.slice_widget.enable_slicing()


