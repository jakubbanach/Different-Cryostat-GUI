from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolBar, QStatusBar, QMainWindow, QFileDialog, QTableWidgetItem)
from PyQt6.QtGui import QIcon, QAction, QFont
import time
import pandas as pd
import numpy as np
import pyqtgraph as pg
import sys


class App(QDialog):
    def __init__(self):
        super(App, self).__init__()
        self.initUI()

    def initUI(self):
        # adding different styles?
        self.originalPalette = QApplication.palette()
        self.setWindowTitle('DATAPLOT')
        self.setWindowIcon(QIcon('./agh.png'))

        menuButtonFile = QPushButton("File")
        menuButtonFile.setDefault(True)

        menuButtonEdit = QPushButton("Edit")
        menuButtonEdit.setDefault(True)

        menuButtonOptions = QPushButton("Options")
        menuButtonOptions.setDefault(True)

        menuButtonAbout = QPushButton("About")
        menuButtonAbout.setDefault(True)

        self.selectDataGroupBox()
        self.resultingChartGroupBox()

        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.addWidget(menuButtonFile)
        self.toolbarLayout.addWidget(menuButtonEdit)
        self.toolbarLayout.addWidget(menuButtonOptions)
        self.toolbarLayout.addWidget(menuButtonAbout)
        self.toolbarLayout.addStretch(1)

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.toolbarLayout, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.selectDataWidget, 1, 0)
        self.mainLayout.addWidget(self.resultingChartWidget, 1, 1)
        self.setLayout(self.mainLayout)

    # functions must be here??
    def movingAvg(self, data, window_length = 25):
        return np.convolve(data, np.ones(window_length), 'valid') / window_length

    def openFile(self):
        try:
            self.pathToFile = QFileDialog.getOpenFileName()[0]
            self.updateTextTable(self.pathToFile)
        except:
            fileName = self.pathToFile
            print(fileName.rpartition('/')[-1])

    def stopReadingFile(self):
        fileName = self.pathToFile
        if fileName != '':
            self.label.setText("Reading stopped: %s" % fileName.rpartition('/')[-1])
        else:
            self.label.setText("NO FILE SELECTED, CLICK Load Data to load your file")
        self.xCombo.clear()
        self.yCombo.clear()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)

    def makeGraph(self):
        self.graphWidget.clear()
        x = self.allData[self.xCombo.currentText()].to_numpy()
        y = self.allData[self.yCombo.currentText()].to_numpy()

        self.graphWidget.setXRange(0.99 * min(x), 1.01 * max(x))
        self.graphWidget.setYRange(0.99 * min(y), 1.01 * max(y))
        self.graphWidget.addLegend(pen=pg.mkPen(color='k', width=2), brush=pg.mkBrush(color=(211, 211, 211)),
                                   frame=True, labelTextColor='k', labelTextSize='12pt')

        self.graphWidget.plot(x, y, pen=None, symbol='o', symbolSize=10, symbolBrush='b', name=self.yCombo.currentText())
        self.graphWidget.plot(self.movingAvg(x), self.movingAvg(y), pen=pg.mkPen(color=(255, 0, 0), width=2), name='mean(' + self.yCombo.currentText() + ')')

        self.graphWidget.setLabel('left', self.yCombo.currentText(), **{'color': 'b', 'font-size': '16px'})
        self.graphWidget.setLabel('bottom', self.xCombo.currentText(), **{'color': 'b', 'font-size': '16px'})


    def updateTextTable(self, fileName):
        if fileName != '':
            self.label.setText("Read file: %s" % fileName.rpartition('/')[-1])
        else:
            self.label.setText("NO FILE SELECTED, CLICK Load Data to load your file")
        self.label.adjustSize()

    def dataLoad(self):
        fileName = self.pathToFile
        self.updateTextTable(fileName)
        if fileName != '':
            self.allData = pd.read_csv(fileName, delimiter='[\t |,]', usecols=lambda x: x not in ['yyyy-mm-dd', 'hh:mm:ss.ccccc'], engine='python')
            if self.allData.size == 0:
                return
            self.allData.fillna('', inplace=True)
            self.columns = self.allData.columns.tolist()
            self.headers = self.allData.columns.values.tolist()
            self.xCombo.clear()
            self.xCombo.addItems(self.headers)
            self.yCombo.clear()
            self.yCombo.addItems(self.headers)

            self.tableWidget.setRowCount(self.allData.shape[0])
            self.tableWidget.setColumnCount(self.allData.shape[1])
            self.tableWidget.setHorizontalHeaderLabels(self.allData.columns)

            for row in self.allData.iterrows():
                values = row[1]
                for col_index, value in enumerate(values):
                    if isinstance(value, (float, int)):
                        value = '{0:0,.8f}'.format(value)
                    self.tableItem = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row[0], col_index, self.tableItem)

            # # QTimer.singleShot(5000, self.dataLoad)
            # print('reading all data')
            # try:
            #     all_data = pd.read_csv(self.pathToFile, delim_whitespace=True, usecols=lambda x: x not in ['yyyy-mm-dd', 'hh:mm:ss.ccccc'])
            # # except:
            # #     print("No data loaded")
            #     if all_data.size == 0:
            #         return
            #     all_data.fillna('', inplace=True)

            #     self.tableWidget.setRowCount(all_data.shape[0]+1)
            #     self.tableWidget.setColumnCount(all_data.shape[1])
            #     self.tableWidget.setHorizontalHeaderLabels(all_data.columns)
            #     self.numbers_of_rows = self.tableWidget.rowCount()
            #     print(self.numbers_of_rows)
            #     for row in all_data.iterrows():
            #         values = row[1]
            #         for col_index, value in enumerate(values):
            #             if isinstance(value, (float, int)):
            #                 value = '{0:0,.8f}'.format(value)
            #             self.tableItem = QTableWidgetItem(str(value))
            #             self.tableWidget.setItem(row[0], col_index, self.tableItem)
            #     # print(all_data)
            #     # headers = all_data.columns.values.tolist()
            #     # print(headers)
            #     print("Loaded: ")
            #     # Rekurencyjne wykonywanie funkcji
            #     # QTimer.singleShot(5000, self.afterFileIsLoaded(all_data))
            # except:
            #     print("No data loaded")

    # def afterFileIsLoaded(self, all_data):
    #     print("HERE WILL BE A RECURENT FUNCTION, SO THAT WE WILL NOT USE WHILE")
    #     time.sleep(10)
    #     self.numbersOfRows = self.tableWidget.rowCount()
    #     try:
    #         #loading file once again, but only last new rows
    #         new_data = pd.read_csv(self.pathToFile, delimiter=r"\s+", delim_whitespace=True, skiprows=self.numbersOfRows, names=all_data.columns)
    #     except:
    #         print("something wrong")
    #         time.sleep(10)
    #     #the size of the file doesn't change
    #     if new_data.size == 0:
    #         print("Nothing changed")
    #     else:
    #         new_data.fillna('', inplace=True)
    #         print(new_data)
    #         self.tableWidget.setRowCount(new_data.shape[0] + self.numbersOfRows)
    #         for row in new_data.iterrows():
    #             values = row[1]
    #             for col_index, value in enumerate(values):
    #                 if isinstance(value, (float, int)):
    #                     value = '{0:0,.8f}'.format(value)
    #                 self.tableItem = QTableWidgetItem(str(value))
    #                 self.tableWidget.setItem(row[0] + self.numbersOfRows, col_index, self.tableItem)
    #         all_data = all_data.append(new_data, ignore_index = True)
    #     print(all_data)
    #     # QTimer.singleShot(5000, self.afterFileIsLoaded(all_data))
    #         # all_data = pd.concat([all_data, new_data])
    #         # self.tableWidget.setRowCount(all_data.shape[0])

    def selectDataGroupBox(self):
        self.selectDataWidget = QGroupBox("Select data:")

        self.tableWidget = QTableWidget(10, 5)

        self.label = QLabel("File")
        self.pathToFile = ''

        self.readButton = QPushButton("&Load Data")
        self.readButton.clicked.connect(self.openFile)

        self.showButton = QPushButton("&Show")
        self.showButton.clicked.connect(self.dataLoad)

        self.stopButton = QPushButton("&Stop")
        self.stopButton.clicked.connect(self.stopReadingFile)
        # self.stopButton.clicked.connect(self.updateTextTable)

        self.xCombo = QComboBox()
        self.yCombo = QComboBox()

        self.plotButton = QPushButton("&Plot Data")
        self.plotButton.clicked.connect(self.makeGraph)

        self.layout = QVBoxLayout()
        widgets = [self.readButton, self.showButton, self.stopButton, self.label, self.tableWidget,
                   self.xCombo, self.yCombo, self.plotButton]
        for widget in widgets:
            if widget == self.label:
                widget.setMaximumWidth(300)
                self.layout.addWidget(widget)
                continue
            if widget == self.tableWidget:
                self.tableWidget.setFixedSize(300, 300)
                self.layout.addWidget(self.tableWidget)
                continue
            widget.setFixedWidth(150)
            self.layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)
            # widget.setAlignment(Qt.AlignVCenter)

        # self.layout.addStretch(1)
        self.selectDataWidget.setLayout(self.layout)

    def resultingChartGroupBox(self):
        self.resultingChartWidget = QGroupBox("Resulting chart:")
        self.graphWidget = pg.PlotWidget()

        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        self.graphWidget.setGeometry(10 , 10, 500, 600)
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.getAxis('left').setPen('k')
        self.graphWidget.getAxis('left').setTextPen('k')
        self.graphWidget.getAxis('left').setFont(font)
        self.graphWidget.getAxis('bottom').setPen('k')
        self.graphWidget.getAxis('bottom').setTextPen('k')
        self.graphWidget.getAxis('bottom').setFont(font)

        layout = QHBoxLayout()
        layout.addWidget(self.graphWidget)
        # layout.addStretch(1)
        self.resultingChartWidget.setLayout(layout)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = App()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())        