from typing import List
from PyQt5.QtCore import Qt, pyqtSignal
import serial.tools.list_ports
from data import ControllerState, Position
from PyQt5.QtWidgets import (
    QHBoxLayout, 
	QVBoxLayout,
    QPushButton,
    QWidget, 
	QLabel,
    QComboBox
)
from controller import Controller

class PnPStateWidget(QWidget):
    """
    Widget for displaying the Pick and Place (PnP) machine state, controller state,
    connection status, and current position. Handles serial port connection and updates UI accordingly.

    Attributes:
        _controller (Controller):
            Controller thats allows this object to send commands to the machine
            and receives information from it.
        _connected (bool):
            Indicates if the PnP is connected ans communicating to the ESP32.
            Allows the UI to display the correct info.
    """
    pnpDoneSignal = pyqtSignal() 

    def __init__(self):
        """
        Initialize the PnPStateWidget, set up the UI, and prepare connection controls.
        """
        super().__init__()

        #main relevant attributes 
        self._controller = Controller()
        self._connected = False 

        #Initialisation of the main layout
        layout = QVBoxLayout()
        connectionLayout = QHBoxLayout()
        self._connectButton = QPushButton("Connect")
        self._connectButton.clicked.connect(self._toggleConnect)
        self._connectButton.setEnabled(False)
        
        
        #initialisation of the connection status layout
        ports = self._scanSerialPorts()
        self._portOptions = QComboBox(self)
        self._portOptions.addItems(ports)
        self._connectionLabel = QLabel()
        self._connectionLabel.setStyleSheet("background-color: red; border-radius: 10px; max-width: 20px; max-height: 20px;")
        connectionLayout.addWidget(self._connectButton)
        connectionLayout.addWidget(QLabel("Port : "), 1)
        connectionLayout.addWidget(self._portOptions, 4)
        connectionLayout.addWidget(self._connectionLabel, 2)

        #initialisation of the PnP info status layout
        self._machineStateLabel = QLabel("Machine State : -")
        self._machineStateLabel.setAlignment(Qt.AlignCenter) 
        self._controllerStateLabel = QLabel("Controller State : -")
        self._controllerStateLabel.setAlignment(Qt.AlignCenter) 
        self._position = Position(0,0,0,0)
        self._positionLabel = QLabel(f"Position : -")
        self._positionLabel.setAlignment(Qt.AlignCenter) 
        layout.addLayout(connectionLayout)
        layout.addWidget(self._machineStateLabel)
        layout.addWidget(self._controllerStateLabel)
        layout.addWidget(self._positionLabel)
        self.setLayout(layout)




    def updateState(self):
        """
        Update the UI to reflect the current machine state, controller state and position.
        """

        #checks the connection status
        if not self._controller.isConnected:
            if self._connected:
                self.setDisconnected()

        elif not self._connected:
            self.setConnected()

        state_m = self._controller.getMachineState()
        self._machineStateLabel.setText(f"Machine State : {state_m}")
        state_c = self._controller.getControllerState()
        self._controllerStateLabel.setText(f"Controller State : {state_c}")
        self._position = self._controller.getGripperPosition()
        self._positionLabel.setText(f"Position : {self._position.x:.2f}, {self._position.y:.2f},"
                                     + f" {self._position.z:.2f}, {self._position.yaw:.2f}")
        
        #listenner for when the PnP is DONE with placing components
        #emits a signal for the control panel
        if state_c == ControllerState.DONE:
            self.pnpDoneSignal.emit()
            print("PnP DONE")
            self._controller.toggleIDLEMode()




    def updateScannedPort(self) :
        """
        Update the list of scanned serial ports and enable/disable the connect button accordingly.
        """
        ports = self._scanSerialPorts()

        if ports:
            if  not self._connectButton.isEnabled():
                self._connectButton.setEnabled(True)
        else :
            if  self._connectButton.isEnabled():
                self._connectButton.setEnabled(False)

        self._portOptions.clear()
        self._portOptions.addItems(ports)




    def getSelectedPort(self) -> str:
        """
        Get the currently selected serial port from the combo box.
        
        Returns:
            str: The selected port name.
        """
        return self._portOptions.currentText()




    def setConnected(self):
        """
        Set the widget state to connected and update the UI indicator.
        """
        self._connected = True
        self._connectionLabel.setStyleSheet("background-color: green; border-radius: 10px; max-width: 20px; max-height: 20px;")




    def setDisconnected(self):
        """
        Set the widget state to disconnected, reset UI labels, and update the indicator.
        """
        self._connected = False
        self._machineStateLabel.setText("Machine State : -")
        self._controllerStateLabel.setText("Controller State : -")
        self._positionLabel.setText("Position : -")
        self._connectionLabel.setStyleSheet("background-color: red; border-radius: 10px; max-width: 20px; max-height: 20px;")




    def _toggleConnect(self):
        """
        Toggle the connection state to the machine. Connects or disconnects based on current state.
        """
        if self._controller.isPortOpen(): 
            self._connectButton.setText("Connect")
            self._controller.disconnectionFromMachine()
            self.setDisconnected()
        else :
            try:
                self._controller.connectionToMachine(self.getSelectedPort(), 115200)
                self.setConnected()
                self._connectButton.setText("Disconnect")
            except Exception as e:
                print(e)




    def _scanSerialPorts(self) -> List[str]:
        """
        Scan for available serial ports, prioritizing Espressif devices.

        Returns:
            List[str]: List of detected serial port connected to an Espressif.
        """
        ports = serial.tools.list_ports.comports()
        # Check by Manufacturer Name
        for port in ports:
            if port.manufacturer and "Espressif" in port.manufacturer:
                return [port.device]
            # Check by USB Vendor ID (Espressif is 0x303A)
            if port.vid == 0x303A:
                return [port.device]
            # Fallback: check description for 'USB Serial' (Common for S3)
            if "USB Serial" in port.description:
                return [port.device]
        return []