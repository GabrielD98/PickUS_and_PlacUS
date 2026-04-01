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
    QSlider
)
from data import MAX_SPEED, Command, CommandId, Position
import utils
from gui.gui_data_manager import GuiDataManager

class CommandWidget(QWidget):

    def __init__(self):
        super().__init__()

        #TODO utiliser des enum de data maybe
        self.on = False 
        self.data_manager = GuiDataManager()
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.stacked_widget = QStackedWidget()
        self.on_active_widget = QWidget()
        self.on_pause_widget = QWidget()
        self.on_active_layout = QHBoxLayout()
        self.on_pause_layout = QHBoxLayout()
        self.on_active_widget.setLayout(self.on_active_layout)
        self.on_pause_widget.setLayout(self.on_pause_layout)
        layout.addWidget(self.stacked_widget)
        self.stacked_widget.setCurrentIndex(0)
        

        self.main_control_button = QPushButton("Start")
        self.continue_button = QPushButton("Continue")
        self.stop_button = QPushButton("Stop")

        self.main_control_button.setEnabled(False)
        self.main_control_button.clicked.connect(self.toggle_start)
        self.continue_button.clicked.connect(self.unpause)
        self.stop_button.clicked.connect(self.stop)

        self.on_active_layout.addWidget(self.main_control_button)
        self.on_pause_layout.addWidget(self.continue_button)
        self.on_pause_layout.addWidget(self.stop_button)
        self.stacked_widget.addWidget(self.on_active_widget)
        self.stacked_widget.addWidget(self.on_pause_widget)




    def start(self):
        self.on = True
        self.main_control_button.setText("Pause")
        
        current_position = self.data_manager.get_gripper_position()
        target = current_position * Position(1,1,0,1)
        command = Command(CommandId.MOVE, MAX_SPEED * 0.5, target, None)
        self.data_manager.queue_command(command)
        self.data_manager.start_pnp()




    def pause(self):
        self.data_manager.pause_pnp()
        self.stacked_widget.setCurrentIndex(1)
        #self.unpause() #reset le pause button, a voir ak la logique globale TODO
    



    def stop(self):
        self.on = False
        self.stacked_widget.setCurrentIndex(0)
        self.main_control_button.setText("Start")
        self.data_manager.transition_to_idle()




    def unpause(self):
        self.data_manager.continue_pnp()
        self.stacked_widget.setCurrentIndex(0)




    def toggle_start(self):
        if self.on: 
            self.pause()
        else:
            self.start()




    def slice_done(self, _):
        self.main_control_button.setEnabled(True)



