from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout, 
	QVBoxLayout,
    QPushButton,
    QWidget, 
    QLineEdit,
	QLabel,
    QStackedWidget,
    QSlider
)
from controller import Controller
from data import Position, MachineState, MAX_SPEED
from command_interface import MoveCommand
from geometry import dimensionLimits
import utils



from geometry import CartesianVelocity

class JogWidget(QWidget):
    """
    Widget for manual jogging and positioning of the gripper in a Pick and Place machine.
    Provides controls for moving in all axes, setting speed, and going to specific positions.

    Attributes:
        _controller (Controller):
            Controller thats allows this object to send commands to the machine
            and receives information from it.
        _jogStep (float):
            the distance traveled by a step querry by the user (mm)
        _speed (float):
            The speed of the gripper movement. (TODO units?)
        _jogEnabled (bool) :
            Indicates if the user is allowed to jog the PnP manually.
    """

    def __init__(self, isMain = True):
        """
        Initialize the JogWidget, set up the UI, and prepare jog controls.
        
        Args:
            isMain (bool, optional): Whether this is the jog widget of the main Window. Defaults to True.
        """
        super().__init__()

        # main relevant attributes 
        defaultSpeed = 50
        self._jogStep = 0.5
        self._controller = Controller()
        self._speed = MAX_SPEED * defaultSpeed/100
        self._jogEnabled = True

        # init of global layout
        self._stackedWidget = QStackedWidget()
        self._interactionWidgets:List[QWidget] = []
        modeOffWidget = QWidget()
        modeOnWidget = QWidget()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._stackedWidget.addWidget(modeOffWidget)
        self._stackedWidget.addWidget(modeOnWidget)
        layout.addWidget(self._stackedWidget)

        # wrapper of the widget to hide buttons
        modeOffLayout = QVBoxLayout()
        modeOffWidget.setLayout(modeOffLayout)
        activate = QPushButton("Activate Jog Mode")
        activate.clicked.connect(lambda : self._activateJogMode())
        modeOffLayout.addWidget(activate)

        goHome = QPushButton("Go Home")
        goHome.clicked.connect(self._goHome)

        # speed slider for gripper movement
        self._speedLabel = QLabel(f"speed : {defaultSpeed}%")
        self._speedSlider = QSlider(Qt.Horizontal)
        self._speedSlider.setRange(10, 100)
        self._speedSlider.setValue(defaultSpeed)
        self._speedSlider.valueChanged.connect(self.updateSpeedSlider)

        # distance of single step entry
        stepEntryLayout = QHBoxLayout()
        stepLabelEntry = QLabel("jog step ")
        self._jogStepEntry = QLineEdit(self)
        self._jogStepEntry.setText("1")
        stepEntryLayout.addWidget(stepLabelEntry)
        stepEntryLayout.addWidget(self._jogStepEntry)

        #buttons for single steps entries and associated function
        incrementLabel = QLabel("Increment Jog")
        yawL = QPushButton("\u2b6e")
        yawR = QPushButton("\u2b6f")
        yPlus = QPushButton("y+")
        yMinus = QPushButton("y-")
        xPlus = QPushButton("x+")
        xMinus = QPushButton("x-")
        zPlus = QPushButton("z+")
        zMinus = QPushButton("z-")
        goToPos = QPushButton("Go to Position")
        deactivate = QPushButton("Deactivate Jog Mode")
        yawL.clicked.connect(lambda : self._rotateLeft())
        yawR.clicked.connect(lambda : self._rotateRight()) 
        yPlus.clicked.connect(lambda : self._movePositiveY()) 
        yMinus.clicked.connect(lambda : self._moveNegativeY()) 
        xPlus.clicked.connect(lambda : self._movePositiveX()) 
        xMinus.clicked.connect(lambda : self._moveNegativeX()) 
        zPlus.clicked.connect(lambda : self._movePositiveZ()) 
        zMinus.clicked.connect(lambda : self._moveNegativeZ()) 
        goToPos.clicked.connect(lambda : self._goToPosition())
        deactivate.clicked.connect(lambda : self._deactivateJogMode())
        
        # Entries for the "go to position" option
        entryLabel = QLabel("Go to Position (mm)")
        self._xEntry = QLineEdit(self)
        self._yEntry = QLineEdit(self)
        self._zEntry = QLineEdit(self)
        self._yawEntry = QLineEdit(self)
        xLabel = QLabel("x")
        yLabel = QLabel("y")
        zLabel = QLabel("z")
        yawLabel = QLabel("yaw")

        # position of the all the global widget dans layout on the control panel 
        modeOnLayout = QVBoxLayout()
        speedLayout = QHBoxLayout()
        upperLayout = QHBoxLayout()
        lowerLayout = QHBoxLayout()
        entryLayout = QHBoxLayout()
        modeOnLayout.addWidget(goHome)
        modeOnLayout.addStretch()
        modeOnLayout.addLayout(speedLayout)
        modeOnLayout.addWidget(incrementLabel)
        modeOnLayout.addLayout(stepEntryLayout)
        modeOnLayout.addLayout(upperLayout)
        modeOnLayout.addLayout(lowerLayout)
        modeOnLayout.addStretch()
        modeOnLayout.addWidget(entryLabel)
        modeOnLayout.addLayout(entryLayout)
        modeOnWidget.setLayout(modeOnLayout)
        modeOnLayout.addWidget(goToPos)

        # if this window is on the main window, hides the manual mode option
        if (isMain):
            modeOnLayout.addStretch()
            modeOnLayout.addWidget(deactivate)
        else :
            self._controller.toggleManualMode()

        # addition of all the individual commands that the user can do in the layouts
        speedLayout.addWidget(self._speedLabel)
        speedLayout.addWidget(self._speedSlider)
        upperLayout.addWidget(xPlus)
        upperLayout.addWidget(yPlus)
        upperLayout.addWidget(zPlus)
        upperLayout.addWidget(yawR)
        lowerLayout.addWidget(xMinus)
        lowerLayout.addWidget(yMinus)
        lowerLayout.addWidget(zMinus)
        lowerLayout.addWidget(yawL)
        entryLayout.addWidget(xLabel, 1)
        entryLayout.addWidget(self._xEntry, 4)
        entryLayout.addWidget(yLabel, 1)
        entryLayout.addWidget(self._yEntry, 4)
        entryLayout.addWidget(zLabel, 1)
        entryLayout.addWidget(self._zEntry, 4)
        entryLayout.addWidget(yawLabel, 1)
        entryLayout.addWidget(self._yawEntry, 4)

        # Adds all the interactions widgets in a list so that they can be activated/deactivated easily
        self._interactionWidgets.append(self._speedLabel)
        self._interactionWidgets.append(self._speedSlider)
        self._interactionWidgets.append(incrementLabel)
        self._interactionWidgets.append(yawL)
        self._interactionWidgets.append(yawR)
        self._interactionWidgets.append(yPlus)
        self._interactionWidgets.append(yMinus)
        self._interactionWidgets.append(xPlus)
        self._interactionWidgets.append(xMinus)
        self._interactionWidgets.append(zPlus)
        self._interactionWidgets.append(zMinus)
        self._interactionWidgets.append(entryLabel)
        self._interactionWidgets.append(xLabel)
        self._interactionWidgets.append(yLabel)
        self._interactionWidgets.append(zLabel)
        self._interactionWidgets.append(yawLabel)
        self._interactionWidgets.append(self._xEntry)
        self._interactionWidgets.append(self._yEntry)
        self._interactionWidgets.append(self._zEntry)
        self._interactionWidgets.append(self._yawEntry)
        self._interactionWidgets.append(goToPos)
        self._interactionWidgets.append(stepLabelEntry)
        self._interactionWidgets.append(self._jogStepEntry)

        if self._controller.homed == False:
            self._deactivateInteractionWidget()

        if not isMain :
            self._stackedWidget.setCurrentIndex(1)




    def updateSpeedSlider(self, value):
        """
        Update the speed value and label when the speed slider is changed.
        
        Args:
            value (int): The new speed value from the slider.
        """
        self._speed = value
        self._speedLabel.setText(f"speed : {str(value)}%")

        return
        #TODO smt like this for slider style, but prettier
        value = self._speedSlider.value()
        maximum = self._speedSlider.maximum()
        
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
        self._speedSlider.setStyleSheet(style)



    
    def getGripperPosition(self) -> Position:
        """
        Get the current position of the gripper from the controller.
        
        Returns:
            Position: The current gripper position.
        """
        return self._controller.getGripperPosition()
    



    def _activateJogMode(self):
        """
        Activate jog mode, enabling manual control of the gripper.
        """
        self._controller.toggleManualMode()
        self._stackedWidget.setCurrentIndex(1)




    def _deactivateJogMode(self):
        """
        Deactivate jog mode, disabling manual control of the gripper.
        """
        self._controller.toggleIDLEMode()
        self._stackedWidget.setCurrentIndex(0)




    def _deactivateInteractionWidget(self):
        """
        Disable all interactive widgets to prevent user input.
        """
        if self._jogEnabled is False:
            return
        for widget in self._interactionWidgets:
            widget.setEnabled(False)
        self._jogEnabled = False
    



    def _activateInteractionWidget(self):
        """
        Enable all interactive widgets to allow user input.
        """
        if self._jogEnabled:
            return
        for widget in self._interactionWidgets:
            widget.setEnabled(True)
        self._jogEnabled = True




    def _validateStepInput(self):
        """
        Validate the jog step input as a float.
        
        Returns:
            float or None: The validated step value, or None if invalid.
        """
        value = self._jogStepEntry.text()
        if not utils.isFloat(value):
            print(f"Invalid input for the step entry. Must be a float, is instead : {value}")
            return None
        return float(value)




    def _movePositiveY(self):
        """
        Move the gripper up (positive Y direction) by the jog step.
        """
        print("up")
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(0, step, 0, 0))




    def _moveNegativeY(self):
        """
        Move the gripper down (negative Y direction) by the jog step.
        """
        print("down")
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(0, -1*step, 0, 0))




    def _moveNegativeX(self):
        """
        Move the gripper left (negative X direction) by the jog step.
        """
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(-1*step, 0, 0, 0))
        print("left")




    def _movePositiveX(self):
        """
        Move the gripper right (positive X direction) by the jog step.
        """
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(step, 0, 0, 0))
        print("right")




    def _moveNegativeZ(self):
        """
        Move the gripper lower (negative Z direction) by the jog step.
        """
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(0, 0, -1*step, 0))
        print("left")




    def _movePositiveZ(self):
        """
        Move the gripper higher (positive Z direction) by the jog step.
        """
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(0, 0, step, 0))
        print("right")




    def _rotateLeft(self):
        """
        Rotate the gripper left (negative yaw) by the jog step.
        """
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(0, 0, 0, -1*step))
        print("rotate left")




    def _rotateRight(self):
        """
        Rotate the gripper right (positive yaw) by the jog step.
        """
        step = self._validateStepInput()
        if step is None:
            return
        currentPos = self.getGripperPosition()
        self._moveGripper(target=currentPos+Position(0, 0, 0, step))
        print("rotate right")




    def _goToPosition(self):
        """
        Move the gripper to a specific position based on user input.
        If an entry is empty or invalid, will be set to the current position of the gripper.
        """
        # reads the user inputs
        xValue = self._xEntry.text()
        yValue = self._yEntry.text()
        zValue = self._zEntry.text()
        yawValue = self._yawEntry.text()
        currentPos = self._controller.getGripperPosition()

        if not utils.isFloat(xValue):
            print(f"Invalid input for the x value. Must be a float, is instead : {xValue}")
            xValue = currentPos.x
            self._xEntry.setText(str(xValue))

        if not utils.isFloat(yValue):
            print(f"Invalid input for the y value. Must be a float, is instead : {yValue}")
            yValue = currentPos.y
            self._yEntry.setText(str(yValue))

        if not utils.isFloat(zValue):
            print(f"Invalid input for the z value. Must be a float, is instead : {zValue}")
            zValue = currentPos.z
            self._zEntry.setText(str(zValue))

        if not utils.isFloat(yawValue):
            print(f"Invalid input for the yaw value. Must be a float, is instead : {yawValue}")
            yawValue = currentPos.yaw
            self._yawEntry.setText(str(yawValue))

        # move the z axis the its highest value before lateral movement (to prevent collisions)
        self._moveGripper(target=Position(currentPos.x, currentPos.y, 0, currentPos.yaw))
        self._moveGripper(target=Position(float(xValue), float(yValue), 0, float(yawValue)))
        self._moveGripper(target=Position(float(xValue), float(yValue), float(zValue), float(yawValue)))




    def _moveGripper(self, target:Position):
        """
        Send a move command to the controller to move the gripper to the target position.
        
        Args:
            target (Position): The target position to move the gripper to.
        """
        target = dimensionLimits(target)
        if self._controller.getMachineState() == MachineState.READY:
            command = MoveCommand(target, CartesianVelocity.uniform(MAX_SPEED * self._speed/100.0))
            self._controller.queueCommand(command)
    



    def _goHome(self):
        """
        Move the gripper to the home position.
        """
        print("Going home")
        self._controller.goHome(endingFunction=self._activateInteractionWidget)

