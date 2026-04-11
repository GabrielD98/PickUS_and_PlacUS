import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QTabWidget
)

class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Scroll bar")
        self.tabs.addTab(self.tab2, "Graphic")

        self.tab1.layout = QVBoxLayout(self.tab1)
        scroll = QScrollArea(self)
        self.tab1.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        scroll.setWidget(scrollContent)

        self.tab2.layout = QVBoxLayout(self.tab2)
        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.tab2.layout.addWidget(self.canvas)

        self.layout.addWidget(self.tabs)