from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QHBoxLayout, 
    QMainWindow, 
    QPushButton,
    QWidget, 
    QFileDialog,
    QLineEdit
)

from PyQt5 import QtWidgets
from pathlib import Path

class Interface(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("My App")

		layout = QHBoxLayout()
		# Add widgets to the layout
		central_widget = QWidget()
		explore_file = QPushButton("Left-Most")
		explore_file.clicked.connect(self.open_file_dialog)
		layout.addWidget(explore_file)
		layout.addWidget(QPushButton("Center"), 1)
		layout.addWidget(QPushButton("Right-Most"), 2)
		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)
		# Set the central widget of the Window.
		#self.setCentralWidget(button)
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

		with open(file_path, "r") as file:
			# Perform file operations inside this block
			content = file.read()
			print(content)

    
    