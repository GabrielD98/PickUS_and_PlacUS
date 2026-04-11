"""
Utility functions and classes for the PickUS & PlacUS application.
Includes layout clearing, type checking, and error window display helpers.
"""
from PyQt5.QtWidgets import (
	QBoxLayout,
    QVBoxLayout,
    QMainWindow, 
    QPushButton,
    QWidget, 
	QLabel,
    QDesktopWidget
)



def clearLayout(layout:QBoxLayout):
    """
    Recursively clear all widgets and nested layouts from a QBoxLayout.
    Deletes widgets and nested layouts to free resources.
    
    Args:
        layout (QBoxLayout): The layout to clear.
    """
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




def isInt(value:str):
    """
    Check if a string value can be converted to an integer.
    
    Args:
        value (str): The string to check.
    Returns:
        bool: True if value is an integer, False otherwise.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False




def isFloat(value:str):
    """
    Check if a string value can be converted to a float.
    
    Args:
        value (str): The string to check.
    Returns:
        bool: True if value is a float, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
    



class ErrorWindow(QMainWindow):
    """
    A simple error message window with a message and an OK button.
    Used to display error messages to the user in a modal dialog.
    """
    def __init__(self, parent=None, error_msg:str = ""):
        """
        Initialize the ErrorWindow with a message and an OK button.
        
        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
            error_msg (str, optional): The error message to display. Defaults to "".
        """
        super().__init__(parent)
        self.setWindowTitle("Calibration Window")
        globalWidget = QWidget()
        globalLayout = QVBoxLayout()
        self.setCentralWidget(globalWidget)
        globalWidget.setLayout(globalLayout)

        msg = QLabel(error_msg)
        button = QPushButton("OK")
        button.clicked.connect(lambda : self.close())

        globalLayout.addWidget(msg)
        globalLayout.addWidget(button)

        globalLayout.setSpacing(50)
        self.center()

    def center(self):
        """
        Calculates the screen center and moves the window there.
        """
        self.adjustSize() 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
           
    def close(self):
        """
        Close the error window and delete it from memory.
        """
        self.deleteLater()
        
