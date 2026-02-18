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

class JogWidget(QWidget):

    def __init__(self, isMain = True):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.interaction_widgets:List[QWidget] = []
        self.interaction_on = True
        mode_off_widget = QWidget()
        mode_on_widget = QWidget()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.stacked_widget.addWidget(mode_off_widget)
        self.stacked_widget.addWidget(mode_on_widget)
        layout.addWidget(self.stacked_widget)

        mode_off_layout = QVBoxLayout()
        mode_off_widget.setLayout(mode_off_layout)
        activate = QPushButton("Activate Jog Mode")
        activate.clicked.connect(lambda : self.turn_on_jog_mode())
        mode_off_layout.addWidget(activate)

        go_home = QPushButton("Go Home")
        go_home.clicked.connect(self.go_home)

        init_speed = 50
        self.speed_label = QLabel(f"speed : {init_speed}%")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(10, 100)
        self.speed_slider.setValue(init_speed)
        self.speed_slider.valueChanged.connect(self.update_speed_slider)

        increment_label = QLabel("Increment Jog")
        yaw_r = QPushButton("\u2b6e")
        yaw_l = QPushButton("\u2b6f")
        y_plus = QPushButton("y+")
        y_minus = QPushButton("y-")
        x_plus = QPushButton("x+")
        x_minus = QPushButton("x-")
        z_plus = QPushButton("z+")
        z_minus = QPushButton("z-")
        go_to_pos = QPushButton("Go to Position")
        deactivate = QPushButton("Deactivate Jog Mode")

        yaw_r.clicked.connect(lambda : self.rotate_right())
        yaw_l.clicked.connect(lambda : self.rotate_left()) 
        y_plus.clicked.connect(lambda : self.go_up()) 
        y_minus.clicked.connect(lambda : self.go_down()) 
        x_plus.clicked.connect(lambda : self.go_left()) 
        x_minus.clicked.connect(lambda : self.go_right()) 
        go_to_pos.clicked.connect(lambda : self.go_to_position())
        deactivate.clicked.connect(lambda : self.turn_off_jog_mode())

        entry_label = QLabel("Go to Position (mm)")
        self.x_entry = QLineEdit(self)
        self.y_entry = QLineEdit(self)
        self.z_entry = QLineEdit(self)
        self.yaw_entry = QLineEdit(self)
        x_label = QLabel("x")
        y_label = QLabel("y")
        z_label = QLabel("z")
        yaw_label = QLabel("yaw")


        mode_on_layout = QVBoxLayout()
        speed_layout = QHBoxLayout()
        upper_layout = QHBoxLayout()
        lower_layout = QHBoxLayout()
        entry_layout = QHBoxLayout()
        mode_on_layout.addWidget(go_home)
        mode_on_layout.addStretch()
        mode_on_layout.addLayout(speed_layout)
        mode_on_layout.addWidget(increment_label)
        mode_on_layout.addLayout(upper_layout)
        mode_on_layout.addLayout(lower_layout)
        mode_on_layout.addStretch()
        mode_on_layout.addWidget(entry_label)
        mode_on_layout.addLayout(entry_layout)
        mode_on_widget.setLayout(mode_on_layout)
        mode_on_layout.addWidget(go_to_pos)

        if (isMain):
            mode_on_layout.addStretch()
            mode_on_layout.addWidget(deactivate)

        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)

        upper_layout.addWidget(x_plus)
        upper_layout.addWidget(y_plus)
        upper_layout.addWidget(z_plus)
        upper_layout.addWidget(yaw_r)
        lower_layout.addWidget(x_minus)
        lower_layout.addWidget(y_minus)
        lower_layout.addWidget(z_minus)
        lower_layout.addWidget(yaw_l)

        entry_layout.addWidget(x_label, 1)
        entry_layout.addWidget(self.x_entry, 4)
        entry_layout.addWidget(y_label, 1)
        entry_layout.addWidget(self.y_entry, 4)
        entry_layout.addWidget(z_label, 1)
        entry_layout.addWidget(self.z_entry, 4)
        entry_layout.addWidget(yaw_label, 1)
        entry_layout.addWidget(self.yaw_entry, 4)

        self.interaction_widgets.append(self.speed_label)
        self.interaction_widgets.append(self.speed_slider)
        self.interaction_widgets.append(increment_label)
        self.interaction_widgets.append(yaw_r)
        self.interaction_widgets.append(yaw_l)
        self.interaction_widgets.append(y_plus)
        self.interaction_widgets.append(y_minus)
        self.interaction_widgets.append(x_plus)
        self.interaction_widgets.append(x_minus)
        self.interaction_widgets.append(z_plus)
        self.interaction_widgets.append(z_minus)
        self.interaction_widgets.append(entry_label)
        self.interaction_widgets.append(x_label)
        self.interaction_widgets.append(y_label)
        self.interaction_widgets.append(z_label)
        self.interaction_widgets.append(yaw_label)
        self.interaction_widgets.append(self.x_entry)
        self.interaction_widgets.append(self.y_entry)
        self.interaction_widgets.append(self.z_entry)
        self.interaction_widgets.append(self.yaw_entry)
        self.interaction_widgets.append(go_to_pos)
        self.deactivate_interaction_widget()

        if not isMain :
            self.stacked_widget.setCurrentIndex(1)
       




    def turn_on_jog_mode(self):
        self.stacked_widget.setCurrentIndex(1)

    def turn_off_jog_mode(self):
        self.stacked_widget.setCurrentIndex(0)

    def deactivate_interaction_widget(self):
        if self.interaction_on is False:
            return
        for widget in self.interaction_widgets:
            widget.setEnabled(False)
        self.interaction_on = False
    
    def activate_interaction_widget(self):
        if self.interaction_on:
            return
        for widget in self.interaction_widgets:
            widget.setEnabled(True)
        self.interaction_on = True


    def go_up(self):
        print("up")

    def go_down(self):
        print("down")

    def go_left(self):
        print("left")

    def go_right(self):
        print("right")

    def rotate_left(self):
        print("rotate left")

    def rotate_right(self):
        print("rotate right")

    def go_to_position(self):
        
        x_value = self.x_entry.text()
        y_value = self.y_entry.text()
        z_value = self.z_entry.text()
        yaw_value = self.yaw_entry.text()

        if not utils.is_int(x_value):
            print(f"Invalid input for the x value. Must be an interger, is instead : {x_value}")
            return
        if not utils.is_int(y_value):
            print(f"Invalid input for the y value. Must be an interger, is instead : {y_value}")
            return
        if not utils.is_int(z_value):
            print(f"Invalid input for the z value. Must be an interger, is instead : {z_value}")
            return
        if not utils.is_int(yaw_value):
            print(f"Invalid input for the yaw value. Must be an interger, is instead : {yaw_value}")
            return
        

        #TODO do smt with these value, should be a controller call


    def go_home(self):
        print("Going home")
        time.sleep(1)
        self.activate_interaction_widget()


    def update_speed_slider(self, value):
        self.speed_label.setText(f"speed : {str(value)}%")

        return
        #TODO smt like this for slider style, but prettier
        value = self.speed_slider.value()
        maximum = self.speed_slider.maximum()
        
        # Calculate percentage for gradient
        percentage = int((value / maximum) * 100) if maximum > 0 else 0
        
        # QSS to fill the groove (blue = filled, grey = empty)
        style = f"""
            QSlider::groove:horizontal {{
                border: 1px solid #bbb;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #337ab7, stop:{percentage/100} #337ab7, 
                    stop:{percentage/100} #e0e0e0, stop:1 #e0e0e0);
                height: 10px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: white;
                border: 1px solid #777;
                width: 14px;
                height: 14px;
                margin-top: -2px;
                margin-bottom: -2px;
                border-radius: 7px;
            }}
        """
        self.speed_slider.setStyleSheet(style)