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

class Window(QMainWindow):

    # Snip...
    def _createToolBars(self):
        # Using a title
        self.fileToolBar = self.addToolBar("File")
        # Using a QToolBar object
        self.editToolBar = QToolBar("Edit", self)
        self.addToolBar(self.editToolBar)
        # Using a QToolBar object and a toolbar area
        self.helpToolBar = QToolBar("Help", self)
        self.addToolBar(Qt.LeftToolBarArea, self.helpToolBar)


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

        menuButton4 = QPushButton("About")
        menuButton4.setDefault(True)

        self.createTopLeftGroupBox()
        # self.createTopRightGroupBox()
        # self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(menuButton1)
        self.topLayout.addWidget(menuButton2)
        self.topLayout.addWidget(menuButton3)
        self.topLayout.addWidget(menuButton4)
        self.topLayout.addStretch(1)

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        self.mainLayout.addWidget(self.bottomRightGroupBox, 1, 1)
        self.setLayout(self.mainLayout)


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
            string = self.path
            print(string.rpartition('/')[-1])

    def stopReading(self, string):
        string = self.path
        self.label.setText("Reading stopped: %s" % string.rpartition('/')[-1])
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
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.graphWidget.plot(self.movingAvg(x), self.movingAvg(y), pen=pen, name='mean(' + self.yCombo.currentText() + ')')

        self.graphWidget.setLabel('left', self.yCombo.currentText(), **{'color': 'b', 'font-size': '16px'})
        self.graphWidget.setLabel('bottom', self.xCombo.currentText(), **{'color': 'b', 'font-size': '16px'})


    def updateTextTable(self, string):
        self.label.setText("Read file: %s" % string.rpartition('/')[-1])
        self.label.adjustSize()

    def dataLoad(self):
        string = self.path
        self.updateTextTable(string)
        self.allData = pd.read_csv(string, delim_whitespace=True, usecols=lambda x: x not in ['yyyy-mm-dd', 'hh:mm:ss.ccccc'])
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

        # QTimer.singleShot(5000, self.dataLoad)
        print('reading all data')
        try:
            all_data = pd.read_csv(self.path, delim_whitespace=True, usecols=lambda x: x not in ['yyyy-mm-dd', 'hh:mm:ss.ccccc'])
        # except:
        #     print("No data loaded")
            if all_data.size == 0:
                return
            all_data.fillna('', inplace=True)

            self.tableWidget.setRowCount(all_data.shape[0]+1)
            self.tableWidget.setColumnCount(all_data.shape[1])
            self.tableWidget.setHorizontalHeaderLabels(all_data.columns)
            self.numbers_of_rows = self.tableWidget.rowCount()
            print(self.numbers_of_rows)
            for row in all_data.iterrows():
                values = row[1]
                for col_index, value in enumerate(values):
                    if isinstance(value, (float, int)):
                        value = '{0:0,.8f}'.format(value)
                    self.tableItem = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row[0], col_index, self.tableItem)
            # print(all_data)
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
        self.numbersOfRows = self.tableWidget.rowCount()
        try:
            #loading file once again, but only last new rows
            new_data = pd.read_csv(self.path, delimiter=r"\s+", delim_whitespace=True, skiprows=self.numbersOfRows, names=all_data.columns)
        except:
            print("something wrong")
            time.sleep(10)
        #the size of the file doesn't change
        if new_data.size == 0:
            print("Nothing changed")
        else:
            new_data.fillna('', inplace=True)
            print(new_data)
            self.tableWidget.setRowCount(new_data.shape[0] + self.numbersOfRows)
            for row in new_data.iterrows():
                values = row[1]
                for col_index, value in enumerate(values):
                    if isinstance(value, (float, int)):
                        value = '{0:0,.8f}'.format(value)
                    self.tableItem = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row[0] + self.numbersOfRows, col_index, self.tableItem)
            all_data = all_data.append(new_data, ignore_index = True)
        print(all_data)
        # QTimer.singleShot(5000, self.afterFileIsLoaded(all_data))
            # all_data = pd.concat([all_data, new_data])
            # self.tableWidget.setRowCount(all_data.shape[0])

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Select data:")

        self.tableWidget = QTableWidget(10, 5)

        self.label = QLabel("File")
        self.path = ''

        self.readButton = QPushButton("&Load Data")
        self.readButton.clicked.connect(self.openFile)
        #ERROR gdy sie kliknie ponownie
        self.showButton = QPushButton("&Show")
        self.showButton.clicked.connect(self.dataLoad)
        # self.testButton = QPushButton("&Plot")
        self.stopButton = QPushButton("&Stop")
        self.stopButton.clicked.connect(self.stopReading)
        # self.stopButton.clicked.connect(self.updateTextTable)

        self.xCombo = QComboBox()
        self.yCombo = QComboBox()

        self.plotButton = QPushButton("&Plot Data")
        self.plotButton.clicked.connect(self.makeGraph)

        self.layout = QVBoxLayout()
        widgets = [self.readButton, self.showButton, self.stopButton, self.label, self.tableWidget,
                   self.xCombo, self.yCombo, self.plotButton]
        for wgt in widgets:
            if wgt == self.label:
                wgt.setMaximumWidth(300)
                self.layout.addWidget(wgt)
                continue
            if wgt == self.tableWidget:
                self.tableWidget.setFixedSize(300, 300)
                self.layout.addWidget(self.tableWidget)
                continue
            wgt.setFixedWidth(150)
            self.layout.addWidget(wgt, alignment=Qt.AlignmentFlag.AlignCenter)
            # wgt.setAlignment(Qt.AlignVCenter)

        # self.layout.addStretch(1)
        self.topLeftGroupBox.setLayout(self.layout)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Resulting chart:")

        # checkBox = QCheckBox("test")

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
        # layout.addWidget(checkBox)
        layout.addWidget(self.graphWidget)
        # layout.addStretch(1)
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
        