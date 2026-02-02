from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QPushButton,QWidget
from PyQt5 import QtWidgets


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        #button = QPushButton("Press Me!")
        #button.clicked.connect(self.handleButton)
        



        layout = QHBoxLayout()
        # Add widgets to the layout
        central_widget = QWidget()
        layout.addWidget(QPushButton("Left-Most"))
        layout.addWidget(QPushButton("Center"), 1)
        layout.addWidget(QPushButton("Right-Most"), 2)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        # Set the central widget of the Window.
        #self.setCentralWidget(button)
        self.showMaximized()
        
    def handleButton(self):
        print('Hello World')

    
    