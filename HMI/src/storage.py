from typing import List
from data import StorageUnit, Piece, Position, StorageState

class Storage :   
    """
    Represents the logic for the storage of the components to place
    This class is a singleton

    Attributes:
        components (dict[str, StorageUnit]): 
            a list a all the components that the storage handles. they will be added by the user in the HMI.
    """

    def __init__(self):
        """
        Initializes the Storage. If an object already has been created, it does nothing.
        """
        if hasattr(self, 'initialized'):
            return
        
        self.components:dict[str, StorageUnit] = {}
        self.initialized = True




    def __new__(cls):
        """
        If a 'Storage' object already has been created, returns the one created before.

        Else, it creates a new 'Storage' object and returns it.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance




    def addComponent(self, piece:Piece, deltaPos:Position, state:StorageState, quantity:int, automatic:bool):
        """
        Adds a component to the storage. This allows the slicer to know wich components will be
        available to place. 

        Parameters:
            piece (Piece): The component's data to be added to this storage unit.
            deltaPos (Position): The offset of each pieces in this storage unit. 
            state (StorageState): The state of this unit -> USING, IGNORE, EMPTY.
            quantity (int): The amount of available components in this unit. 
            automatic (bool): Is the component feeder automatic or not.
        """
        if piece.package in self.components:
            return
        component = StorageUnit(piece=piece, deltaPos=deltaPos, state=state, 
                                quantity=quantity, automatic=automatic)
        self.components[piece] = component




    def removeComponent(self, piece:Piece):
        """
        Removes a component that has been added before by the user. If the component
        is not found, does nothing

        Parameters:
            piece (Piece): The component's data to be removed to this storage unit.
        """
        if not piece in self.components:
            return
        del self.components[piece]




    def getValidComponents(self) -> List[Piece]:
        """
        Returns a list of all the components that can be treated by the slicer. 
        To be valid, the state has to be set to 'USING".

        Returns:
            (List[Piece]): The list of all the valid pieces.
        """
        valid_components:List[Piece] = []
        for component in self.components.values():
            if component.state == StorageState.USING:
                valid_components.append(component.piece)
        return valid_components
        