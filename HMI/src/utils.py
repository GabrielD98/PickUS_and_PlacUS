from PyQt5.QtWidgets import (
	QVBoxLayout,
    QMainWindow, 
    QPushButton,
    QWidget, 
	QLabel,
    QDesktopWidget
)



def clearLayout(layout:QVBoxLayout):
    if layout is None:
        return
    
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            # If the item is a layout (nested layout), clear it recursively
            clearLayout(item.layout())
        del item



def is_int(value:str):
    try:
        int(value)
        return True
    except ValueError:
        return False
    

def is_float(value:str):
    try:
        float(value)
        return True
    except ValueError:
        return False
    









class ErrorWindow(QMainWindow):
    def __init__(self, parent=None, error_msg:str = ""):
        super().__init__(parent)
        self.setWindowTitle("Calibration Window")
        global_widget = QWidget()
        global_layout = QVBoxLayout()
        self.setCentralWidget(global_widget)
        global_widget.setLayout(global_layout)

        msg = QLabel(error_msg)
        button = QPushButton("OK")
        button.clicked.connect(lambda : self.close())

        global_layout.addWidget(msg)
        global_layout.addWidget(button)

        global_layout.setSpacing(50)
        self.center()

    def center(self):
        """Calculates the screen center and moves the window there."""
        self.adjustSize() 

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
           
    
    def close(self):
        self.deleteLater()
        
