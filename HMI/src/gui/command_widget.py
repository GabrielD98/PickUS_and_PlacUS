from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout, 
    QPushButton,
    QWidget, 
    QStackedWidget
)
from controller import Controller
from data import MAX_SPEED, Command, CommandId, Position
from gui.button import Button


class CommandWidget(QWidget):
    """
    Widget for controlling the main Pick and Place (PnP) control process.
    Provides buttons to start, pause, continue, and stop the PnP,
    and manages the UI state accordingly.

    Attributes:
        _controller (Controller):
            Controller thats allows this object to send commands to the machine
            and receives information from it.
        _on (bool):
            indicates if the PnP is current in the process of placing components.
    """

    pnpStartingSignal = pyqtSignal() 


    def __init__(self):
        """
        Initialize the CommandWidget, set up the UI and connect button signals.
        """
        super().__init__()

        # main relevant attributes 
        self._controller = Controller()
        self._on = False

        layout = QHBoxLayout()
        self.setLayout(layout)

        #sets the stacked layout for the different control state
        self._stackedWidget = QStackedWidget()
        self._onActiveWidget = QWidget()
        self._onPauseWidget = QWidget()
        self._onActiveLayout = QHBoxLayout()
        self._onPauseLayout = QHBoxLayout()
        self._onActiveWidget.setLayout(self._onActiveLayout)
        self._onPauseWidget.setLayout(self._onPauseLayout)
        layout.addWidget(self._stackedWidget)
        self._stackedWidget.setCurrentIndex(0)
        
        #setup of the control buttons and widgets
        self._mainControlButton = Button("Start")
        self._continueButton = Button("Continue")
        self._stopButton = Button("Stop")
        self._mainControlButton.setEnabled(False)
        self._mainControlButton.clicked.connect(self._toggleStart)
        self._continueButton.clicked.connect(self._unpause)
        self._stopButton.clicked.connect(self._stop)

        #add the widgets in the desired layout order
        self._onActiveLayout.addWidget(self._mainControlButton)
        self._onPauseLayout.addWidget(self._continueButton)
        self._onPauseLayout.addWidget(self._stopButton)
        self._stackedWidget.addWidget(self._onActiveWidget)
        self._stackedWidget.addWidget(self._onPauseWidget)

        #START BUTTON 
        self._mainControlButton.setCheckable(True)
        self._mainControlButton.qss_style.font_size = "35px"
        self._mainControlButton.qss_style.border_radius = "22px"
        self._mainControlButton.qss_style.font_weight = "bold"
        self._mainControlButton.qss_style.padding = "10px, 10px"

        self._mainControlButton.qss_style.disabled_color =  "#02542E"
        self._mainControlButton.qss_style.background_color = "#02542E"
        self._mainControlButton.qss_style.hover_color = "#048E4D"

        #PAUSE BUTTON
        self._mainControlButton.qss_style.pressed_color =  "#B84D01"
        self._mainControlButton.qss_style.hover_pressed_color = "#E56305"

        self._mainControlButton.commitStyleSheet()

        #STOP BUTTON 
        self._stopButton.qss_style.disabled_color =  "#680707"
        self._stopButton.qss_style.background_color = "#680707"
        self._stopButton.qss_style.hover_color = "#B11B1B"
        
        self._stopButton.commitStyleSheet()

        #CONTINUE BUTTON
        self._continueButton.qss_style.disabled_color =  "#02542E"
        self._continueButton.qss_style.background_color = "#02542E"
        self._continueButton.qss_style.hover_color = "#048E4D"

        self._continueButton.commitStyleSheet()



    def sliceDone(self, _):
        """
        Enable the main control button when a slice operation is done.
        """
        self._mainControlButton.setEnabled(True)



    def pnpDone(self):
        """
        Stop the Pick and Place process when the operation is complete.
        """
        self._stop()


    def _start(self):
        """
        Start the Pick and Place process, update UI, and send the initial command to the controller.
        """
        self._on = True
        self._mainControlButton.setText("Pause")
        self._mainControlButton.setChecked(True)

        current_position = self._controller.getGripperPosition()
        target = current_position * Position(1,1,0,1)
        command = Command(CommandId.MOVE, MAX_SPEED * 0.5, target, None)
        self._controller.queueCommand(command)
        self._controller.startPnP()
        self.pnpStartingSignal.emit()



    def _pause(self):
        """
        Pause the Pick and Place process and update the UI to show pause controls.
        """
        self._mainControlButton.setChecked(True)
        self._controller.pausePnP()
        self._stackedWidget.setCurrentIndex(1)
        #self.unpause() #reset le pause button, a voir ak la logique globale TODO
    



    def _stop(self):
        """
        Stop the Pick and Place process.
        The command queue will be cleared and the UI will be set to its initial sate.
        """
        self._on = False
        self._stackedWidget.setCurrentIndex(0)
        self._mainControlButton.setChecked(False)
        self._mainControlButton.setText("Start")
        self._controller.toggleIDLEMode()




    def _unpause(self):
        """
        Continue the Pick and Place process after a pause.
        """
        self._mainControlButton.setChecked(False)
        self._controller.continuePnP()
        self._stackedWidget.setCurrentIndex(0)




    def _toggleStart(self):
        """
        Toggle between starting and pausing the Pick and Place process based on current state.
        """
        if self._on: 
            self._pause()
        else:
            self._start()
