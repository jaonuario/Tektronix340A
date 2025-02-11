import sys
import numpy as np

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg 

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot(self, x, y, y_min=None, y_max=None):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(x, y)
        if y_min is not None and y_max is not None:
            ax.set_ylim(y_min, y_max)

        self.canvas.draw()




if __name__ == '__main__':
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    app = QApplication(sys.argv)
    window = PlotWidget()
    window.plot(x, y)
    window.setFixedSize(400, 400)
    window.show()
    sys.exit(app.exec())
