from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QColor
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
)
from dataclasses import dataclass


@dataclass
class WidgetConfig:
    image_path: str = '../data/Golden_Roman_Frame.png'
    slices: str = "50 50 50 50" 
    background_color: str = "transparent"
    txt_color: str = "black"
    padding: str = "1px 1px"


class Frame(QFrame):

    def __init__(self, child_widget=None, style=None):
        super().__init__()
        
        self.style_config = style if style else WidgetConfig()

        self.main_layout = QVBoxLayout(self)
        
        self.main_layout.setSpacing(0)

        if child_widget:
            child_widget.setStyleSheet("background: transparent; border: none;")
            self.main_layout.addWidget(child_widget)
            
        self.apply_roman_style()

    def apply_roman_style(self):

        self.setObjectName("RomanFrame")

        border_width = self.style_config.slices.split()[0] + "px"
        self.setStyleSheet(f"""
            QFrame#RomanFrame {{
                border-image: url('{self.style_config.image_path}') {self.style_config.slices} stretch;
                border-width: {border_width};
                border-style: solid;
                background-color: white;
            }}
        """)

    def set_child(self, widget):
        """Allows adding a widget later"""
        self.layout.addWidget(widget)