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
class ButtonStyle:
    background_color:str
    txt_color:str
    border_radius:str 
    padding:str 
    font_size:str 
    font_weight:str
    border:str

    hover_color:str
    pressed_color:str
    hover_pressed_color:str
    padding_top_pressed:str
    padding_bot_pressed:str
    disabled_color:str
    disabled_text_color:str 
 
    current_color:str

    image_path: str = '../data/../data/Light_Bronze_Button.png'
    slices: str = "30 30 30 30" 

    hover_image_path: str = ''
    slices_hover: str = "30 30 30 30" 


class Button(QPushButton):

    def __init__(self, text="Button"):
        super().__init__(text)

        self.qss_style = ButtonStyle (
            background_color="white",
            txt_color="black", 
            border_radius = "0px",
            padding = "8px, 14px",
            font_size = "14px",
            font_weight = "none",
            border = "none",

        # "#CBCBCB" , "#959393" , "#A2A2A2"
            hover_color = "transparent",
            pressed_color = "transparent",
            hover_pressed_color = "transparent",
            padding_top_pressed = "10px",
            padding_bot_pressed = "6px",
            disabled_color = "transparent",
            disabled_text_color = "black",

            current_color = "transparent"
            # Setup animation
            
        )
        self.update_style()
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(300) # 300ms transition
        


    # Define a custom property for the color
    @pyqtProperty(QColor)
    def color(self):
        return QColor(self.qss_style.current_color)




    @color.setter
    def color(self, val:QColor):
        self.qss_style.current_color = val.name()
        self.update_style()

    
    def commitStyleSheet(self):
        # Sync the static color to the active current_color
        self.qss_style.current_color = self.qss_style.background_color
        self.update_style()



    def update_style(self):
        """
        Single source of truth for the stylesheet.
        """
        style = self.qss_style
        # Clean the padding string (PyQt QSS doesn't like the comma)
        clean_padding = style.padding.replace(',', '')

        self.setStyleSheet(f"""
            QPushButton {{
                /* The border-image is drawn ON TOP of the background-color */
                border-image: url('{self.qss_style.image_path}') {self.qss_style.slices} stretch;
                background-color: {style.current_color}; 
                color: {style.txt_color};
                border-radius: {style.border_radius};
                padding: {clean_padding}; 
                font-size: {style.font_size};
                font-weight: {style.font_weight};
                border: {style.border};
                
            }}

            /* Hover state (mouse over) */
            QPushButton:hover {{
                border-image: url('{self.qss_style.hover_image_path}') {self.qss_style.slices_hover} stretch;
                background-color: {style.hover_color}; 

            }}
            
             /* This state stays active after clicking if setCheckable(True) */
            QPushButton:checked {{
                background-color: {style.pressed_color}; 
            }}

            QPushButton:checked:hover {{
                background-color: {style.hover_pressed_color}; 
            }}

            /* Disabled state */
            QPushButton:disabled {{
                background-color: {style.disabled_color}; 
                color: {style.disabled_text_color};
            }}

        """)
