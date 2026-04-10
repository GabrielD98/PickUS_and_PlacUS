from dataclasses import dataclass
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
import utils
from gui.gui_data_manager import GuiDataManager
from gui.button import Button




class CommandWidget(QWidget):

    def __init__(self):
        super().__init__()

        #TODO utiliser des enum de data maybe
        self.on = False 
        self.in_pause = False
        self.data_manager = GuiDataManager()

        layout = QHBoxLayout()
        self.setLayout(layout)
        self.start_button = Button("Start")
        self.pause_button = Button("Pause")

        self.start_button.clicked.connect(self.toggle_start)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setEnabled(False)

        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)


        #START BUTTON 
        # self.start_button.qss_style.background_color =  "#30E993"
        self.start_button.setCheckable(True) # This allows it to stay "Checked"
        self.start_button.qss_style.font_size = "35px"
        self.start_button.qss_style.border_radius = "22px"
        self.start_button.qss_style.font_weight = "bold"
        self.start_button.qss_style.padding = "20px, 20px"
        self.start_button.qss_style.background_color = "#02542E"
        self.start_button.qss_style.hover_color = "#048E4D"
        self.start_button.qss_style.pressed_color =  "#910D0D"
        self.start_button.qss_style.hover_pressed_color = "#C41D1D"
        self.start_button.commitStyleSheet()

        #PAUSE BUTTON 
        self.pause_button.setCheckable(True) # This allows it to stay "Checked"
        self.pause_button.qss_style.font_size = "35px"
        self.pause_button.qss_style.border_radius = "22px"
        self.pause_button.qss_style.font_weight = "bold"
        self.pause_button.qss_style.padding = "20px, 20px"
        self.pause_button.qss_style.background_color = "#B84D01"
        self.pause_button.qss_style.disabled_color =  "#B84D01"
        self.pause_button.qss_style.hover_color = "#E56305"
        self.pause_button.qss_style.pressed_color = "#02542E"
        self.pause_button.qss_style.hover_pressed_color = "#048E4D"
        self.pause_button.commitStyleSheet()


    def start(self):
        self.on = True
        self.start_button.setChecked(True)
        self.start_button.setText("Stop")
        self.pause_button.setEnabled(True)
        self.data_manager.start_pnp()




    def stop(self):
        self.on = False
        self.start_button.setChecked(False)
        self.start_button.setText("Start")
        self.pause_button.setEnabled(False)
        self.unpause() #reset le pause button, a voir ak la logique globale TODO
    



    def pause(self):
        self.in_pause = True
        self.pause_button.setChecked(True)
        self.pause_button.setText("Continue")
        self.data_manager.pause_pnp()




    def unpause(self):
        self.in_pause = False
        self.pause_button.setChecked(False)
        self.pause_button.setText("Pause")
        self.data_manager.continue_pnp()




    def toggle_start(self):
        # Let the button's checked state drive the logic
        if self.start_button.isChecked():
            self.start()
        else:
            self.stop()




    def toggle_pause(self):
        if self.pause_button.isChecked():
            self.pause()
        else:
            self.unpause()