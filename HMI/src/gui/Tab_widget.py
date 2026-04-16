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
        self._commandsTab.setStyleSheet("background-image: url('../data/Slice_Background_Vf.png') 0 0 0 0 stretch;background-position: center; border: none;")
        scroll = QScrollArea(self)
        commandsLayout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background:transparent")
       # scroll.setStyleSheet("background-image: url('../data/big_Background_Scroll.png') 100 100 100 100 stretch; background-repeat: no-repeat;" \
       # "background-position: center; border: none;")

        scrollContent = QWidget(scroll)
        scrollContent.setStyleSheet("background-color: transparent;")

        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        scroll.setWidget(scrollContent)

        graphLayout = QVBoxLayout(self._graphTab)
        self._graphTab.setLayout(graphLayout)
        self._graphTab.setStyleSheet("background-image: url('../data/Slice_Background_Vf.png') 0 0 0 0 stretch;background-position: center; border: none;")

        self.canvas = FigureCanvas(Figure(figsize=(5, 4), dpi=100))
        self.canvas.setStyleSheet("background:transparent;")

        # Ensure the figure itself is initialized as transparent
        self.canvas.figure.patch.set_facecolor('none')
        self.canvas.figure.patch.set_alpha(0.0)

        self.ax = self.canvas.figure.add_subplot(111)
        # Make the actual plot area (axes) transparent from the start
        self.ax.patch.set_facecolor('none')
        self.ax.patch.set_alpha(0.0)

        graphLayout.addWidget(self.canvas)
        globalLayout.addWidget(self.tabs)
    

        TAB_STYLE = """
            QTabWidget::pane {
                background-color: transparent; 
            }
        
            QTabBar::tab {
                min-width: 150px;           /* Adjust this for wider tabs */
                min-height: 50px;           /* Adjust this for taller tabs */
                padding: 10px;              /* Internal spacing for text */
                font-size: 18px;
                color: rgba(209, 177, 118, 255);
                border-image: url("../data/Button_Bronze_Frame.png") "100 100 100 100" stretch;
            }

            QTabBar::tab:selected {
                min-width: 150px;           /* Adjust this for wider tabs */
                min-height: 50px;           /* Adjust this for taller tabs */
                padding: 10px;              /* Internal spacing for text */
                font-size: 18px;
                color: rgba(209, 177, 118, 255);
                border-image: url("../data/Tab_Background.png") "100 100 100 100" stretch;
            }

            QTabBar::tab:hover {
                min-width: 150px;           /* Adjust this for wider tabs */
                min-height: 50px;           /* Adjust this for taller tabs */
                padding: 10px;              /* Internal spacing for text */
                font-size: 18px;
                color: rgba(209, 177, 118, 255);
                border-image: url("../data/Tab_Background.png") "100 100 100 100" stretch;
            }
            """
        self.tabs.setStyleSheet(TAB_STYLE)
