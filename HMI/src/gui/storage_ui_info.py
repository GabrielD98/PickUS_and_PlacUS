from PyQt5.QtWidgets import (
    QHBoxLayout, 
    QPushButton,
    QWidget, 
	QLabel,
    QStackedWidget
)
from data import *

class StorageUiInfo(QWidget):
    """
    Widget for displaying and managing the UI information of a storage piece.
    Shows the name, state, quantity, and automatic status, and allows updating these fields.

    Attributes:
        button (QPushButton):
            A reference to the button of this space. Use to set the pieces informations.
            #TODO should be signal for less spagetti.
        _states (dict[StorageState, str]):
            The different states that the storage can have (for display purposes)
        _piece (Piece):
            The associated with this storage space.
        _added (bool):
            boolean that indicates if this piece as been initialized in the storage.

    """
    def __init__(self, piece:Piece, button:QPushButton):
        """
        Initialize the StorageUiInfo widget, set up the UI, and prepare display fields.
        
        Args:
            piece (Piece): The piece to display information for.
            button (QPushButton): A reference to the button associated with this piecs.
                                  Allows the user to add/modify a piece in the storage.
                                  Also allows the main UI to modify it.
        """
        super().__init__()
        self._states = {
            StorageState.EMPTY : "EMPTY",
            StorageState.IGNORE : "IGNORE",
            StorageState.USING : "USING"
        }

        # Relevent attributes 
        self._piece = piece
        self.button = button
        self._added:bool = False

        # initialisation of important storage data for this piece.
        self._stackedWidget = QStackedWidget()
        self._name:str = piece.package
        self._quantity:int = -1
        self.nameLabel = QLabel(self._name)
        self.stateLabel = QLabel("state : -")
        self.quantityLabel = QLabel("quantity : -")
        self.automaticLabel = QLabel("automatic : -")

        activeWidget = QWidget()
        activeLayout = QHBoxLayout()
        activeLayout.setSpacing(30)
        activeLayout.addWidget(self.nameLabel)
        activeLayout.addWidget(self.stateLabel)
        activeLayout.addWidget(self.quantityLabel)
        activeLayout.addWidget(self.automaticLabel)
        activeWidget.setLayout(activeLayout)

        # Layout when the piece is not added yet 
        inactiveWidget = QWidget()
        inactiveLayout = QHBoxLayout()
        additionLabel = QLabel("(Not Added)")
        additionLabel.setStyleSheet("color: red;") 
        inactiveWidget.setLayout(inactiveLayout)

        inactiveLayout.addWidget(QLabel(self._name))
        inactiveLayout.addWidget(additionLabel)

        self._stackedWidget.addWidget(inactiveWidget)
        self._stackedWidget.addWidget(activeWidget)
        layout = QHBoxLayout()
        layout.addWidget(self._stackedWidget)
        self.setLayout(layout)




    def updateAll(self, name:str, state:StorageState, quantity:int, auto:bool):
        """
        Update all fields of the storage info widget and switch to the active display.
        
        Args:
            name (str): The name of the piece.
            state (StorageState): The state of the storage.
            quantity (int): The quantity of the piece.
            auto (bool): Whether the storage is set to automatic.
        """
        self.updateName(name)
        self.updateState(state)
        self.updateQuantity(quantity)
        self.updateAutomaticState(auto)
        self._stackedWidget.setCurrentIndex(1)
        self.button.setText("Change")




    def updateName(self, newName:str):
        """
        Update the name of the piece in the UI.
        
        Args:
            new_name (str): The new name to display.
        """
        self._name = newName
        self.nameLabel.setText(self._name)




    def updateState(self, newState:StorageState):
        """
        Update the state of the storage in the UI.
        
        Args:
            new_state (StorageState): The new state to display.
        """
        self.stateLabel.setText("state : " + self._states[newState])




    def updateQuantity(self, newQuantity:int):
        """
        Update the quantity of the piece in the UI.
        
        Args:
            new_quantity (int): The new quantity to display.
        """
        self._quantity = newQuantity
        self.quantityLabel.setText(f"quantity : {self._quantity}")




    def updateAutomaticState(self, newState:bool):
        """
        Update the automatic state of the piece in the UI.
        
        Args:
            new_auto_state (bool): The new automatic state to display.
        """
        newText = "automatic : False"
        if newState == True:
            newText = "automatic : True"
        self.automaticLabel.setText(newText)



