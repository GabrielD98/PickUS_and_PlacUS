from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import (
    QHBoxLayout, 
	QVBoxLayout,
    QMainWindow, 
    QPushButton,
    QWidget, 
	QLabel,
    QDesktopWidget
)
from data import *
from gui.jog_widget import JogWidget
from controller import Controller
import json


JSON_KEY = "Calibration"


class CalibrationWindow(QMainWindow):
    """
    Window thats opens when the user wants to calibrate the position
    of the PCB.

    Attributes:
        position (Position): 
            A reference to the position of the gripper that will be saved 
            by the main UI. TODO maybe shoud be a signal.
        _controller (Controller):
            Controller thats allows this object to send commands to the machine
            and receives information from it.
        _jog_widget (JogWidget):
            Widget that alows the user to send specific position and movement 
            commands to the machine.

    """
    def __init__(self, parent=None, position:Position = None):
        """
        Initialize the CalibrationWindow.
        
        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
            position (Position, optional): The position object to update with calibration values. Defaults to None.
        """
        super().__init__(parent)

        # main relevant attributes 
        self.position = position
        self._controller = Controller()
        self._jogWidget = JogWidget(isMain=False)

        # gloabal layout and widget of this window
        self.setWindowTitle("Calibration Window")
        globalWidget = QWidget()
        globalLayout = QVBoxLayout()
        self.setCentralWidget(globalWidget)
        globalWidget.setLayout(globalLayout)

        # bottom section with control buttons (load, save and confirm)
        instruction = QLabel("Please put the end of the gripper on the calibration spot, then click 'confirm'")
        self._loadJSONbutton = QPushButton("Load Previous Calibration")
        self._saveJSONButton = QPushButton("Save Current Calibration")
        self._calibrateButton = QPushButton("Confirm")
        self._loadJSONbutton.clicked.connect(lambda : self._loadPreviousCalibration())
        self._saveJSONButton.clicked.connect(lambda : self._saveCurrentCalibration())
        self._calibrateButton.clicked.connect(lambda : self._setCalibrationPosition())

        # set the widget in the desired order of the layout        
        JSONLayout = QHBoxLayout()
        JSONLayout.setSpacing(30)
        JSONLayout.addWidget(self._saveJSONButton)
        JSONLayout.addWidget(self._loadJSONbutton)   
        globalLayout.setSpacing(20)
        globalLayout.addWidget(instruction)
        globalLayout.addWidget(self._jogWidget)
        globalLayout.addLayout(JSONLayout)
        globalLayout.addWidget(self._calibrateButton)
        self._center()




    def closeEvent(self, event: QEvent):
        """
        Override the default close event handler to ensure calibration position is set before closing.
        """
        self._setCalibrationPosition()




    def _loadPreviousCalibration(self):
        """
        Load the previous calibration values from the calibration JSON file and
        set the values in the jog widget entries if available.
        """

        data = self._readJSONData()

        key = JSON_KEY
        if key in data:
            self._jogWidget.x_entry.setText(data[key]["x"])
            self._jogWidget.y_entry.setText(data[key]["y"])
            self._jogWidget.z_entry.setText(data[key]["z"])
            self._jogWidget.yaw_entry.setText(data[key]["yaw"])




    def _saveCurrentCalibration(self):
        """
        Save the current gripper position as calibration values to the calibration JSON file.
        """

        data = self._readJSONData()

        if JSON_KEY not in data:
            data[JSON_KEY] = {}

        position = self._controller.get_gripper_position()
        data[JSON_KEY]["x"] = str(round(position.x, 2))
        data[JSON_KEY]["y"] = str(round(position.y, 2))
        data[JSON_KEY]["z"] = str(round(position.z, 2))
        data[JSON_KEY]["yaw"] = str(round(position.yaw, 2))

        with open(CALIB_PATH, "w") as file:
            json.dump(data, file, indent=4)





    def _readJSONData(self):
        """
        Read calibration data from the calibration JSON file. If the file does not exist or is corrupted,
        it creates a new file with an empty dictionary.
        
        Returns:
            dict: The calibration data.
        """
        try:
            with open(CALIB_PATH, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create the file with an empty dictionary if it's missing or corrupted
            data = {}
            with open(CALIB_PATH, 'w') as file:
                json.dump(data, file)
        
        return data





    def _center(self):
        """
        Calculates the screen center and moves the window there.
        """
        self.adjustSize() 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    
    def _setCalibrationPosition(self):
        """
        Set the calibration position by updating the referenced position object
        with the current values from the jog widget, then close the window.
        """
        position = self._jogWidget.get_gripper_position()

        #we need to keep position as a reference
        self.position.x = position.x
        self.position.y = position.y
        self.position.z = position.z
        self.position.yaw = position.yaw
        
        print("calibration ended successfully")

        #delete the window when the position is saved
        self.deleteLater()
        
