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
)

from PyQt5 import QtWidgets
from pathlib import Path

class Interface(QMainWindow):
	def __init__(self):
		super().__init__()
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





		explore_file = QPushButton("Open .pos file")
		explore_file.clicked.connect(self.open_file_dialog)
		self.file_label = QLabel('No File Selected', alignment=Qt.AlignLeft|Qt.AlignVCenter)
		self.file_label.setStyleSheet("color: black; background-color: white")
		file_layout = QHBoxLayout()
		file_layout.addWidget(explore_file, 1)
		file_layout.addWidget(self.file_label, 5)
		left_layout.addLayout(file_layout, 1)


		#TODO delete label
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		pieces_layout = QHBoxLayout()
		pieces_layout.addWidget(white_label)
		left_layout.addLayout(pieces_layout, 6)

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
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		commands_layout = QHBoxLayout()
		commands_layout.addWidget(white_label)
		left_layout.addLayout(commands_layout, 2)


		#TODO delete label
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		state_layout = QHBoxLayout()
		state_layout.addWidget(white_label)
		right_layout.addLayout(state_layout, 4)



		#TODO delete label
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		home_layout = QHBoxLayout()
		home_layout.addWidget(white_label)
		right_layout.addLayout(home_layout, 3)

		#TODO delete label
		white_label = QLabel(self)
		white_label.setStyleSheet("background-color: white; border: 1px solid black;") 
		jog_layout = QHBoxLayout()
		jog_layout.addWidget(white_label)
		right_layout.addLayout(jog_layout, 4)


		img_label = QLabel(self)
		pixmap = QPixmap("../data/a_joyful_Julius_C.png")
		img_label.setPixmap(pixmap)
		right_layout.addWidget(img_label, 4)

		
		self.setCentralWidget(global_widget)

		self.showMaximized()
		return

		file_pos_layout = QHBoxLayout()
		file_pos_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

		file_position_widget = QWidget()
		explore_file = QPushButton("Open .pos file")
		explore_file.clicked.connect(self.open_file_dialog)
		self.file_label = QLabel('No File Selected', alignment=Qt.AlignCenter)
		self.file_label.setStyleSheet("color: black; background-color: white")
		file_pos_layout.addWidget(explore_file)
		file_pos_layout.addWidget(self.file_label)
		file_position_widget.setLayout(file_pos_layout)
		self.setCentralWidget(file_position_widget)
		self.setStyleSheet(
			"""
			QMainWindow {{
				border-image: url({image_path}) 0 0 0 0 stretch stretch;
			}}
			""".format(image_path="../data/a_joyful_Julius_C.png")
		)


		self.showMaximized()



	def handleButton(self):
		print('Hello World')

	def open_file_dialog(self):
		filename, _ = QFileDialog.getOpenFileName(
			parent=self,               
			caption="Select a File",
			directory="../data/", 
			filter="All Files (*.pos)" 
		)

		if not filename:
			return
			# Display the selected file path
		file_path = str(Path(filename))
		self.file_label.setText(file_path)

		with open(file_path, "r") as file:
			# Perform file operations inside this block
			content = file.read()
			print(content)

    
    