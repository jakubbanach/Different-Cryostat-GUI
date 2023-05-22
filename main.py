from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolBar, QStatusBar, QMainWindow, QFileDialog, QTableWidgetItem)
from PyQt6.QtGui import QIcon, QAction, QFont
import random
import time


import pandas as pd
import numpy as np
import pyqtgraph as pg

class Window(QMainWindow):

    # Snip...
    def _createToolBars(self):
        # Using a title
        fileToolBar = self.addToolBar("File")
        # Using a QToolBar object
        editToolBar = QToolBar("Edit", self)
        self.addToolBar(editToolBar)
        # Using a QToolBar object and a toolbar area
        helpToolBar = QToolBar("Help", self)
        self.addToolBar(Qt.LeftToolBarArea, helpToolBar)


class App(QDialog):
    def __init__(self):
        super(App, self).__init__()
        self.initUI()

    def initUI(self):
        # adding different styles?
        QApplication.setStyle('windowsvista')
        self.originalPalette = QApplication.palette()
        self.setWindowTitle('DATAPLOT')
        self.setWindowIcon(QIcon('./agh.png'))

        menuButton1 = QPushButton("File")
        menuButton1.setDefault(True)

        menuButton2 = QPushButton("Edit")
        menuButton2.setDefault(True)

        menuButton3 = QPushButton("Options")
        menuButton3.setDefault(True)

        self.createTopLeftGroupBox()
        # self.createTopRightGroupBox()
        # self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addWidget(menuButton1)
        topLayout.addWidget(menuButton2)
        topLayout.addWidget(menuButton3)
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 1, 1)
        mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)


    def movingAvg(self, data, window_length = 25):
        return np.convolve(data, np.ones(window_length), 'valid') / window_length


    # functions must be here??
    def openFile(self):
        try:
            self.path = QFileDialog.getOpenFileName()[0]
            self.updateTextTable(self.path)
            # try:
            #     all_data = pd.read_csv(self.path, delimiter=' ')
            #     self.tableWidget.setRowCount(all_data.shape[0])
            #     self.tableWidget.setColumnCount(all_data.shape[1])
            #     self.tableWidget.setHorizontalHeaderLabels(all_data.columns)
            # except:
            #     print("File not exist")
        except:
            ### maybe print only the last part of the path?
            print(self.path)

    def updateText(self):
        #random_text = random.randint(0, 100)
        #self.label.setText("Your random number is %d" % random_text)
        self.label.setText("Stop reading file: "+ self.path)
        self.label.adjustSize()
        # T[C] Ux[V]
        self.col1 = self.allData[self.columns[0]].to_numpy()
        self.col2 = self.allData[self.columns[2]].to_numpy()
        print(type(self.col1))
        print(type(self.col2))
        # T_A[K] T_B[K] CNT sr860x[V] sr860y[V] sr860f[Hz] sr860sin[V]
        self.graphWidget.plot(self.col1, self.col2)

    def makeGraph(self):
        self.graphWidget.clear()
        x = self.allData[self.xCombo.currentText()].to_numpy()
        y = self.allData[self.yCombo.currentText()].to_numpy()

        self.graphWidget.setXRange(0.99 * min(x), 1.01 * max(x))
        self.graphWidget.setYRange(0.99 * min(y), 1.01 * max(y))

        scatter = pg.ScatterPlotItem(size=5, brush=pg.mkBrush(0, 0, 255))
        scatter.setData(x, y)
        self.graphWidget.addItem(scatter)

        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.graphWidget.plot(self.movingAvg(x), self.movingAvg(y), pen=pen)

        self.graphWidget.setLabel('left', self.yCombo.currentText(), **{'color': 'b', 'font-size': '16px'})
        self.graphWidget.setLabel('bottom', self.xCombo.currentText(), **{'color': 'b', 'font-size': '16px'})
        self.graphWidget.addLegend()

    def updateTextTable(self, string):
        self.label.setText("Your file: %s" % string.rpartition('/')[-1])
        self.label.adjustSize()

    def dataLoad(self):
        self.allData = pd.read_csv(self.path, delimiter=' ')
        if self.allData.size == 0:
            return
        self.allData.fillna('', inplace=True)
        # self.allData.replace("~!@#$%^&*()=+~\|}{';:- /?>,<", "")
        self.columns = self.allData.columns.tolist()
        self.headers = self.allData.columns.values.tolist()
        print(self.columns)
        self.xCombo.addItems(self.headers)
        self.yCombo.addItems(self.headers)

        self.tableWidget.setRowCount(self.allData.shape[0])
        self.tableWidget.setColumnCount(self.allData.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(self.allData.columns)

        for row in self.allData.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.8f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row[0], col_index, tableItem)

        # QTimer.singleShot(5000, self.dataLoad)
        print('reading all data')
        try:
            all_data = pd.read_csv(self.path, delimiter=' ')
        # except:
        #     print("No data loaded")
            if all_data.size == 0:
                return
            all_data.fillna('', inplace=True)

            self.tableWidget.setRowCount(all_data.shape[0]+1)
            self.tableWidget.setColumnCount(all_data.shape[1])
            self.tableWidget.setHorizontalHeaderLabels(all_data.columns)
            numbersOfRows = self.tableWidget.rowCount()
            print(numbersOfRows)
            for row in all_data.iterrows():
                values = row[1]
                for col_index, value in enumerate(values):
                    if isinstance(value, (float, int)):
                        value = '{0:0,.8f}'.format(value)
                    tableItem = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row[0], col_index, tableItem)
            print(all_data)
            # headers = all_data.columns.values.tolist()
            # print(headers)
            print("Loaded: ")
            # Rekurencyjne wykonywanie funkcji
            # QTimer.singleShot(5000, self.afterFileIsLoaded(all_data))
        except:
            print("No data loaded")

    def afterFileIsLoaded(self, all_data):
        print("HERE WILL BE A RECURENT FUNCTION, SO THAT WE WILL NOT USE WHILE")
        time.sleep(10)
        numbersOfRows = self.tableWidget.rowCount()
        try:
            #loading file once again, but only last new rows
            new_data = pd.read_csv(self.path, delimiter=' ', skiprows=numbersOfRows, names=all_data.columns)
        except:
            print("something wrong")
            time.sleep(10)
        #the size of the file doesnt change
        if new_data.size == 0:
            print("Nothing changed")
        else:
            new_data.fillna('', inplace=True)
            print(new_data)
            self.tableWidget.setRowCount(new_data.shape[0] + numbersOfRows)
            for row in new_data.iterrows():
                values = row[1]
                for col_index, value in enumerate(values):
                    if isinstance(value, (float, int)):
                        value = '{0:0,.8f}'.format(value)
                    tableItem = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row[0]+numbersOfRows, col_index, tableItem)
            all_data = all_data.append(new_data, ignore_index = True)
        print(all_data)
        # QTimer.singleShot(5000, self.afterFileIsLoaded(all_data))
            # all_data = pd.concat([all_data, new_data])
            # self.tableWidget.setRowCount(all_data.shape[0])

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Select data:")

        radioButton1 = QRadioButton("parse with . dots")
        radioButton2 = QRadioButton("parse with , commas")
        radioButton3 = QRadioButton("parse with ' ' blank space")
        radioButton3.setChecked(True)

        self.tableWidget = QTableWidget(10, 5)

        self.label = QLabel("file")
        self.path = ''

        self.readButton = QPushButton("&Load Data")
        self.readButton.clicked.connect(self.openFile)

        #ERROR gdy sie kliknie ponownie
        self.showButton = QPushButton("&Show")
        self.showButton.clicked.connect(self.dataLoad)
        self.testButton = QPushButton("&Plot")
        self.testButton = QPushButton("&Stop")
        self.testButton.clicked.connect(self.updateText)

        self.xCombo = QComboBox()
        self.yCombo = QComboBox()

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(self.readButton)
        layout.addWidget(self.showButton)
        layout.addWidget(self.testButton)
        layout.addWidget(self.label)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.xCombo)
        layout.addWidget(self.yCombo)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Resulting chart:")

        checkBox = QCheckBox("test")

        self.graphWidget = pg.PlotWidget()

        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.getAxis('left').setPen('k')
        self.graphWidget.getAxis('left').setTextPen('k')
        self.graphWidget.getAxis('left').setFont(font)
        self.graphWidget.getAxis('bottom').setPen('k')
        self.graphWidget.getAxis('bottom').setTextPen('k')
        self.graphWidget.getAxis('bottom').setFont(font)




        self.plotButton = QPushButton("&Plot Data")
        self.plotButton.clicked.connect(self.makeGraph)

        layout = QHBoxLayout()
        layout.addWidget(checkBox)
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.plotButton)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = App()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

    #app = QtWidgets.QApplication(sys.argv)
    #ex = Ui_MainWindow()
    #w = QtWidgets.QMainWindow()
    #ex.setupUi(w)
    #w.show()
    #sys.exit(app.exec_())
        