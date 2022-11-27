import matplotlib.pyplot as plt
from PyQt6 import QtWidgets
import pyqtgraph as pg


class LiveGraph(pg.PlotWidget):

    def __init__(self):
        super(LiveGraph, self).__init__()
        print("I am class type LiveGraph")

        self.GraphWidget = pg.PlotWidget()

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        self.GraphWidget.plot(hour, temperature)
