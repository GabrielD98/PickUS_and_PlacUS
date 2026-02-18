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
from pnp_state_widget import PnPStateWidget
from slicer import Slicer
from storage import Storage
from data import *
from typing import List
from storage_window import StorageWindow
from storage_ui_info import StorageUiInfo
from jog_widget import JogWidget
from command_widget import CommandWidget
import utils
		
		
		


class Interface(QMainWindow):
	def __init__(self):
		super().__init__()
		self.storage_window:StorageWindow = None
		self.controller = Controller()
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


		#TODO delete label
		#FILE READING LAYOUT
		self.pieces_layout = QVBoxLayout()
		left_layout.addLayout(self.pieces_layout, 3)

		#TODO delete label
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		calibration_layout = QHBoxLayout()
		calibration_layout.addWidget(white_label)
		left_layout.addLayout(calibration_layout, 2)


		#TODO delete label
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		slice_layout = QHBoxLayout()
		slice_layout.addWidget(white_label)
		left_layout.addLayout(slice_layout, 2)


		#TODO delete label
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		step_layout = QHBoxLayout()
		step_layout.addWidget(white_label)
		left_layout.addLayout(step_layout, 6)


		#TODO delete label
		commands_layout = QHBoxLayout()
		commands_layout.addWidget(CommandWidget())
		left_layout.addLayout(commands_layout, 2)


		#TODO delete label
		state_layout = QHBoxLayout()
		state_layout.addWidget(PnPStateWidget(self.controller))
		right_layout.addLayout(state_layout, 1)



		#TODO delete label
		#white_label = QLabel(self)
		#white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		jog_layout = QHBoxLayout()
		jog_layout.addWidget(JogWidget())
		right_layout.addLayout(jog_layout, 4)


		img_label = QLabel(self)
		pixmap = QPixmap("../data/a_joyful_Julius_C.png")
		img_label.setPixmap(pixmap)
		right_layout.addWidget(img_label, 2)

		
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

		


	def analyse_file(self):
		pieces = FileInterpreter().readPositionFile(self.file_path)
		if pieces is None:
			return
		self.pieces = self.get_all_unique_piece(pieces)
		self.update_piece_list()
		self.analyse_button.setEnabled(False)
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
		self.storage_window = StorageWindow()
		self.storage_window.set_inputs(info)
		self.storage_window.show()


