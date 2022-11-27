import matplotlib.pyplot as plt
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
from random import *


class exampleGraph(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(exampleGraph, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

class LiveGraph(pg.PlotWidget):

    def __init__(self):
        super(LiveGraph, self).__init__()
        print("I am class type LiveGraph")

        self.xLabel = 'x'
        self.yLabel = 'y'

        self.GraphWidget = pg.PlotWidget()
        self.GraphWidget.setBackground("w")

        self.hour = []
        self.temperature = []

        for i in range(10):
            [h, t] = [np.random.rand(), np.random.rand()]
            self.hour.append(h)
            self.temperature.append(t)
            i += 1

        self.graph = self.GraphWidget.plot(self.hour, self.temperature, symbol='o', pen=None)

        styles = {'color': 'b', 'font-size': '20px'}
        self.GraphWidget.setLabel('bottom', self.xLabel, **styles)
        self.GraphWidget.setLabel('left', self.yLabel, **styles)
        self.GraphWidget.showGrid(x=True, y=True)

        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(500)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

    def update_plot_data(self):
        print(self.hour)
        # self.hour = self.hour[1:]
        # self.hour.append(np.random.rand())

        # self.temperature = self.temperature[1:]
        # self.temperature.append(np.random.rand())
        # print(self.hour)
        # print(self.temperature)
        # self.graph.setData(self.hour, self.temperature)
        # self.GraphWidget.plot(self.hour, self.temperature, symbol='o', pen=None)