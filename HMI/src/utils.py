from PyQt5.QtWidgets import QVBoxLayout

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