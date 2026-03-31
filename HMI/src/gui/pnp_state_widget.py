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
import serial.tools.list_ports
from typing import List

class PnPStateWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.dataManager = GuiDataManager()
        self.connected = False 

        connection_layout = QHBoxLayout()
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connect)
        self.connect_button.setEnabled(False)

        ports = self.scan_serial_ports()
        self.port_options = QComboBox(self)
        self.port_options.addItems(ports)
        self.connection_label = QLabel()
        self.connection_label.setStyleSheet("background-color: red; border-radius: 10px; max-width: 20px; max-height: 20px;")
        connection_layout.addWidget(self.connect_button)
        connection_layout.addWidget(QLabel("Port : "), 1)
        connection_layout.addWidget(self.port_options, 4)
        connection_layout.addWidget(self.connection_label, 2)

        self.machine_state_label = QLabel("Machine State : -")
        self.machine_state_label.setAlignment(Qt.AlignCenter) 
        self.controller_state_label = QLabel("Controller State : -")
        self.controller_state_label.setAlignment(Qt.AlignCenter) 
        self.position = Position(0,0,0,0)
        self.position_label = QLabel(f"Position : -")
        self.position_label.setAlignment(Qt.AlignCenter) 
        

        layout.addLayout(connection_layout)
        layout.addWidget(self.machine_state_label)
        layout.addWidget(self.controller_state_label)
        layout.addWidget(self.position_label)
        self.setLayout(layout)
        

    def update_state(self):

        if not self.dataManager.is_connected:
            if self.connected:
                self.set_disconnected()

        elif not self.connected:
            self.set_connected()

        state = self.dataManager.get_machine_state()
        self.machine_state_label.setText(f"Machine State : {state}")
        state = self.dataManager.get_controller_state()
        self.controller_state_label.setText(f"Controller State : {state}")
        self.position = self.dataManager.get_gripper_position()
        self.position_label.setText(f"Position : {self.position.x:.2f}, {self.position.y:.2f},"
                                     + f" {self.position.z:.2f}, {self.position.yaw:.2f}")
        #print("STATE : ", self.dataManager.controller.getState())
        

    def scan_serial_ports(self) -> List[str]:
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




    def update_scanned_port(self) :
        ports = self.scan_serial_ports()

        if ports:
            if  not self.connect_button.isEnabled():
                self.connect_button.setEnabled(True)
        else :
            if  self.connect_button.isEnabled():
                self.connect_button.setEnabled(False)

        self.port_options.clear()
        self.port_options.addItems(ports)


    def get_selected_port(self) -> str:
        return self.port_options.currentText()


    def set_connected(self):
        self.connected = True
        self.connection_label.setStyleSheet("background-color: green; border-radius: 10px; max-width: 20px; max-height: 20px;")

    def set_disconnected(self):
        self.connected = False
        self.machine_state_label.setText("Machine State : -")
        self.controller_state_label.setText("Controller State : -")
        self.position_label.setText("Position : -")
        self.connection_label.setStyleSheet("background-color: red; border-radius: 10px; max-width: 20px; max-height: 20px;")


    def toggle_connect(self):
        
        if self.dataManager.is_port_open(): 
            self.connect_button.setText("Connect")
            self.dataManager.disconnect()
            self.set_disconnected()
        else :
            try:
                self.dataManager.connect_to_pnp(self.get_selected_port())
                self.set_connected()
                self.connect_button.setText("Disconnect")
            except Exception as e:
                print(e)