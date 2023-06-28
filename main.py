from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolBar, QStatusBar, QMainWindow, QFileDialog, QTableWidgetItem)
from PyQt6.QtGui import QIcon, QAction, QFont
import pandas as pd
import numpy as np
import pyqtgraph as pg
import sys
import time
from PyQt6.QtGui import QGuiApplication


class App(QDialog):
    def __init__(self):
        super(App, self).__init__()
        self.initUI()
        self.isPlottingGoing = True

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
        self.showButton.setStyleSheet("background-color: white; border-color: black; font: bold 14px;")


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


    def clearGraph(self):
        self.graphWidget.clear()

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
            self.showButton.setStyleSheet("background-color: yellow; border-color: black; font: bold 14px;")

            for row in self.allData.iterrows():
                values = row[1]
                for col_index, value in enumerate(values):
                    if isinstance(value, (float, int)):
                        value = '{0:0,.8f}'.format(value)
                    self.tableItem = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row[0], col_index, self.tableItem)

    def updateGraph(self):
        self.makeGraph()
        QGuiApplication.processEvents()     #powoduje, ze wywoluje sie plot w funkcji
        while self.isPlottingGoing:
            time.sleep(5)
            self.numbersOfRows = self.tableWidget.rowCount()
            try:
                new_data = pd.read_csv(self.pathToFile, delimiter='[\t |,]', usecols=lambda x: x not in ['yyyy-mm-dd', 'hh:mm:ss.ccccc'], engine='python', skiprows=self.numbersOfRows, names=self.allData.columns)
            except:
                print("Error in reading new file")
                time.sleep(10)
            if new_data.size != 0:
                new_data.fillna('', inplace=True)
                self.tableWidget.setRowCount(new_data.shape[0] + self.numbersOfRows)

                for row in new_data.iterrows():
                    values = row[1]
                    for col_index, value in enumerate(values):
                        if isinstance(value, (float, int)):
                            value = '{0:0,.8f}'.format(value)
                        self.tableItem = QTableWidgetItem(str(value))
                        self.tableWidget.setItem(row[0] + self.numbersOfRows, col_index, self.tableItem)
                self.allData = pd.concat([self.allData, new_data], ignore_index=True)
                self.tableWidget.setRowCount(self.allData.shape[0])
                self.makeGraph()
                QGuiApplication.processEvents()
            if self.stopButton.clicked:
                self.isPlottingGoing = False

    def selectDataGroupBox(self):
        self.selectDataWidget = QGroupBox("Select data:")

        self.tableWidget = QTableWidget(10, 5)
        
        self.label = QLabel("File:")
        self.pathToFile = ''

        self.readButton = QPushButton("&1. Load Data")
        self.readButton.setStyleSheet("background-color: white; border-color: black; font: bold 14px;")
        self.readButton.clicked.connect(self.openFile)

        self.showButton = QPushButton("&2. Show")
        self.showButton.setStyleSheet("background-color: white; border-color: black; font: bold 14px;")
        self.showButton.clicked.connect(self.dataLoad)

        self.xComboLabel = QLabel("Choose X:")
        self.xCombo = QComboBox()
        self.yComboLabel = QLabel("Choose Y:")
        self.yCombo = QComboBox()

        self.plotButton = QPushButton("&3. Plot Data")
        self.plotButton.setStyleSheet("background-color: lightgreen; border-color: black; font: bold 14px;")

        ### tu bylo testowane co sie dzieje po kliknieciu przycisku

        # if self.plotButton.pressed:
        #     self.makeGraph
        #     print("After button is pressed")
        #     time.sleep(5)
        #     self.makeGraph
        #     print("After button is pressed")
        #     time.sleep(5)
        #     self.makeGraph
        # ###Tu mozna sprobowac dodac wlasnie i ewentualnie w innych miejscach tego False
        #     self.isPlottingGoing = True

        self.plotButton.clicked.connect(self.makeGraph)
        #self.plotButton.clicked.connect(self.updateGraph)  #funkcja do odswiezania wykresow, na razie zakomentowana, zeby pozostale rzeczy dzialaly
        self.stopButton = QPushButton("&4. Stop")
        self.stopButton.clicked.connect(self.stopReadingFile)
        self.stopButton.setStyleSheet("background-color: red; border-color: black; font: bold 14px;")
        # self.stopButton.clicked.connect(self.updateTextTable)

        self.layout = QVBoxLayout()
        widgets = [self.readButton, self.showButton, self.label, self.tableWidget,
                   self.xComboLabel, self.xCombo, self.yComboLabel, self.yCombo, self.plotButton, self.stopButton]
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

        self.clearButton = QPushButton("& Clear chart")
        self.clearButton.setStyleSheet("background-color: lightblue; border-color: black; font: bold 14px;")
        self.clearButton.clicked.connect(self.clearGraph)
        self.clearButton.setFixedWidth(150)

        layout = QVBoxLayout()
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.clearButton, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout.addStretch(1)
        self.resultingChartWidget.setLayout(layout)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = App()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())        