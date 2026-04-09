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
    image_path: str = '../data/Widgets_Frame.png'
    slices: str = "45 45 45 45" 
    background_color: str = "transparent"
    txt_color: str = "black"
    padding: str = "0px 0px"


class Frame(QFrame):

    def __init__(self, child_widget=None, style=None):
        super().__init__()
        
        self.style_config = style if style else WidgetConfig()

        self.main_layout = QVBoxLayout(self)
        
        # Remove all spacing that might cause gaps
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 2. Inner Container
        self.inner_container = QWidget()
        self.inner_layout = QVBoxLayout(self.inner_container)
        self.inner_layout.setContentsMargins(0, 0, 0, 0) 

        self.main_layout.addWidget(self.inner_container)

        if child_widget:
            child_widget.setStyleSheet("background: transparent; border: none;")
            self.inner_layout.addWidget(child_widget)
            
        self.apply_roman_style()

    def apply_roman_style(self):
        border_width = self.style_config.slices.split()[0] + "px"
        self.setStyleSheet(f"""
            QFrame {{
                border-image: url('{self.style_config.image_path}') {self.style_config.slices} stretch;
                border-width: {border_width};
                border-style: solid;
                background-color: transparent;
            }}
        """)
        self.inner_container.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                margin: -{border_width}; 
            }}
        """)

    def set_child(self, widget):
        """Allows adding a widget later"""
        self.layout.addWidget(widget)