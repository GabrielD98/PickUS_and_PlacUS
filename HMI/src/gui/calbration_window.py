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
	QCheckBox,
    QDesktopWidget
)


from gui.gui_data_manager import GuiDataManager
from storage import Storage
from data import *
from typing import List
import utils
from gui.storage_ui_info import StorageUiInfo
from gui.jog_widget import JogWidget
import json


JSON_KEY = "Calibration"


class CalibrationWindow(QMainWindow):
    def __init__(self, parent=None, position:Position = None):
        super().__init__(parent)

        self.position = position
        self.dataManager = GuiDataManager()

        self.setWindowTitle("Calibration Window")
        self.jog_widget = JogWidget(isMain=False)
        global_widget = QWidget()
        global_layout = QVBoxLayout()
        self.setCentralWidget(global_widget)
        global_widget.setLayout(global_layout)

        
        instruction = QLabel("Please put the end of the gripper on the calibration spot, then click 'confirm'")
        self.load_json_button = QPushButton("Load Previous Calibration")
        self.save_json_button = QPushButton("Save Current Calibration")
        self.calibrate_button = QPushButton("Confirm")
        self.load_json_button.clicked.connect(lambda : self.load_previous_calibration())
        self.save_json_button.clicked.connect(lambda : self.save_current_calibration())
        self.calibrate_button.clicked.connect(lambda : self.set_calibration_position())
        
        
        global_layout.addWidget(instruction)
        global_layout.addWidget(self.jog_widget)
        global_layout.addWidget(self.load_json_button)
        global_layout.addWidget(self.save_json_button)
        global_layout.addWidget(self.calibrate_button)
        self.center()


    def load_previous_calibration(self):

        with open(CALIB_PATH, 'r') as file:
            data = json.load(file)

        key = JSON_KEY
        if key in data:
            self.jog_widget.x_entry.setText(data[key]["x"])
            self.jog_widget.y_entry.setText(data[key]["y"])
            self.jog_widget.z_entry.setText(data[key]["z"])
            self.jog_widget.yaw_entry.setText(data[key]["yaw"])



    def save_current_calibration(self):
        with open(CALIB_PATH, "r") as file:
            data = json.load(file)


        position = self.dataManager.get_gripper_position()
        data[JSON_KEY]["x"] = str(round(position.x, 2))
        data[JSON_KEY]["y"] = str(round(position.y, 2))
        data[JSON_KEY]["z"] = str(round(position.z, 2))
        data[JSON_KEY]["yaw"] = str(round(position.yaw, 2))

        with open(CALIB_PATH, "w") as file:
            json.dump(data, file, indent=4)



    def center(self):
        """Calculates the screen center and moves the window there."""
        self.adjustSize() 

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
            
    
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