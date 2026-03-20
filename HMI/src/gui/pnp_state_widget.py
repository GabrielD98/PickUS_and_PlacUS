import time
from typing import List
from PyQt5.QtCore import Qt
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
	QInputDialog,
    QStackedWidget,
    QSlider,
    QComboBox
)

import utils
from data import Position
from gui.gui_data_manager import GuiDataManager
from PyQt5.QtSerialPort import QSerialPortInfo
import serial.tools.list_ports

class PnPStateWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.dataManager = GuiDataManager()

        connection_layout = QHBoxLayout()
        ports = self.scan_serial_ports()
        self.port_options = QComboBox(self)
        self.port_options.addItems(ports)
        self.connection_label = QLabel()
        self.connection_label.setStyleSheet("background-color: red; border-radius: 10px; max-width: 20px; max-height: 20px;")
        connection_layout.addWidget(QLabel("Port : "), 1)
        connection_layout.addWidget(self.port_options, 4)
        connection_layout.addWidget(self.connection_label, 2)

        self.state_label = QLabel("State : -")
        self.state_label.setAlignment(Qt.AlignCenter) 
        self.position = Position(0,0,0,0)
        self.position_label = QLabel(f"Position : {self.position.x}, {self.position.y},"
                                     + f" {self.position.z}, {self.position.yaw}")
        self.position_label.setAlignment(Qt.AlignCenter) 
        

        layout.addLayout(connection_layout)
        layout.addWidget(self.state_label)
        layout.addWidget(self.position_label)
        self.setLayout(layout)
        

    def update_state(self):
        state = self.dataManager.get_machine_state()
        self.state_label.setText(f"State : {state}")
        self.position = self.dataManager.get_gripper_position()
        self.position_label.setText(f"Position : {self.position.x:.2f}, {self.position.y:.2f},"
                                     + f" {self.position.z:.2f}, {self.position.yaw:.2f}")
        print("STATE : ", self.dataManager.controller.getState())
        

    def scan_serial_ports(self) -> List[str]:
        ports = QSerialPortInfo.availablePorts()
        open_ports:List[str] = []
        for port in ports:
            if port.isBusy() == False:
                open_ports.append(port.portName())
        
        return open_ports
    


    def update_scanned_port(self) :
        ports = self.scan_serial_ports()
        self.port_options.clear()
        self.port_options.addItems(ports)


    def get_selected_port(self) -> str:
        return self.port_options.currentText()


    def set_connected(self):
        self.connection_label.setStyleSheet("background-color: green; border-radius: 10px; max-width: 20px; max-height: 20px;")

    def set_disconnected(self):
        self.connection_label.setStyleSheet("background-color: red; border-radius: 10px; max-width: 20px; max-height: 20px;")
