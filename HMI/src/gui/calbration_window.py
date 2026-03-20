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



class CalibrationWindow(QMainWindow):
    def __init__(self, parent=None, position:Position = None):
        super().__init__(parent)

        self.position = position

        self.setWindowTitle("Calibration Window")

        global_widget = QWidget()
        global_layout = QVBoxLayout()
        self.setCentralWidget(global_widget)
        global_widget.setLayout(global_layout)

        instruction = QLabel("Please put the end of the gripper on the calibration spot, then click 'confirm'")
        self.calibrate_button = QPushButton("Confirm")
        self.calibrate_button.clicked.connect(lambda : self.set_calibration_position())
        self.jog_widget = JogWidget(isMain=False)
        global_layout.addWidget(instruction)
        global_layout.addWidget(self.jog_widget)
        global_layout.addWidget(self.calibrate_button)


    
    def set_calibration_position(self):
        position = self.jog_widget.get_gripper_position()

        #we need to keep position as a reference
        self.position.x = position.x
        self.position.y = position.y
        self.position.z = position.z
        self.position.yaw = position.yaw
        
        print("calibration ended successfully")
        print(self.position)
        self.deleteLater()
        


    def closeEvent(self, event: QEvent):
        """Override the default close event handler."""
        self.set_calibration_position()