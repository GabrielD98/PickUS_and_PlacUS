from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QTabWidget
)

class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        globalLayout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self._commandsTab = QWidget()
        self._graphTab = QWidget()

        self.tabs.addTab(self._commandsTab, "Scroll bar")
        self.tabs.addTab(self._graphTab, "Graphic")

        commandsLayout = QVBoxLayout(self._commandsTab)
        self._commandsTab.setLayout(commandsLayout)
        scroll = QScrollArea(self)
        commandsLayout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        scroll.setWidget(scrollContent)

        graphLayout = QVBoxLayout(self._graphTab)
        self._graphTab.setLayout(graphLayout)
        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        graphLayout.addWidget(self.canvas)

        globalLayout.addWidget(self.tabs)