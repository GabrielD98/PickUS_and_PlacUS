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
    padding_top_pressed:str
    padding_bot_pressed:str

    disabled_color:str
    disabled_text_color:str 

    current_color:str



class Button(QPushButton):

    def __init__(self, text="Button"):
        super().__init__(text)

        self.qss_style = ButtonStyle (
            background_color="white",
            txt_color="black", 
            border_radius = "4px",
            padding = "8px, 16px",
            font_size = "14px",
            font_weight = "none",
            border = "none",

            hover_color = "#CBCBCB",
            pressed_color = "#959393",
            padding_top_pressed = "10px",
            padding_bot_pressed = "6px",

            disabled_color = "#A2A2A2",
            disabled_text_color = "black",

            current_color = "white"
            # Setup animation
            
        )
        self._color = QColor("#3498db")
        self.update_style()
        self.animation = QPropertyAnimation(self, b"color")
        self.animation.setDuration(300) # 300ms transition
        



    # Define a custom property for the color
    @pyqtProperty(QColor)
    def color(self):
        return QColor(self.qss_style.current_color)




    @color.setter
    def color(self, val):
        self.qss_style.current_color = val
        self.update_style()




    def update_style(self):
        style = self.qss_style

        self.setStyleSheet(f"""
            /* Base state for all buttons */
            QPushButton {{
                background-color: {style.current_color}; 
                color: {style.txt_color};
                border-radius: {style.border_radius};
                padding: {style.padding};
                font-size: {style.font_size};
                font-weight: {style.font_weight};
                border: {style.border};
                
            }}
            /* Pressed state (mouse click) */
            QPushButton:pressed {{
                background-color: {style.pressed_color}; 
                /*padding-top: {style.padding_top_pressed}; 
                padding-bottom: {style.padding_bot_pressed};*/
            }}

            /* Disabled state */
            QPushButton:disabled {{
                background-color: {style.disabled_color}; 
                color: {style.disabled_text_color};
            }}
        """)




    def enterEvent(self, event):
        # Mouse Hover Start
        self.animation.stop()
        self.animation.setEndValue(QColor(self.qss_style.hover_color))
        self.animation.start()
        super().enterEvent(event)





    def leaveEvent(self, event):
        # Mouse Hover End
        self.animation.stop()
        self.animation.setEndValue(QColor(self.qss_style.background_color))
        self.animation.start()
        super().leaveEvent(event)


















    def commitStyleSheet(self):
        style = self.qss_style

        self.setStyleSheet(f"""
            /* Base state for all buttons */
            QPushButton {{
                background-color: {style.background_color}; 
                color: {style.txt_color};
                border-radius: {style.border_radius};
                padding: {style.padding};
                font-size: {style.font_size};
                font-weight: {style.font_weight};
                border: {style.border};
                
            }}

            /* Hover state (mouse over) */
            QPushButton:hover {{
                background-color: {style.hover_color}; 
            }}

            /* Pressed state (mouse click) */
            QPushButton:pressed {{
                background-color: {style.pressed_color}; 
                /*padding-top: {style.padding_top_pressed}; 
                padding-bottom: {style.padding_bot_pressed};*/
            }}

            /* Disabled state */
            QPushButton:disabled {{
                background-color: {style.disabled_color}; 
                color: {style.disabled_text_color};
            }}
        """)
