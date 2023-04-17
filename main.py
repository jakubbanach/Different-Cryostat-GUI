from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolBar, QStatusBar, QMainWindow)
from PyQt6.QtGui import QIcon, QAction

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
        QApplication.setStyle('windowsvista')
        self.originalPalette = QApplication.palette()
        self.setWindowTitle('DATAPLOT')
        self.setWindowIcon(QIcon('./agh.jpg'))

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


    # functions must be here??
    def openFile(self):
        try:
            self.path = QFileDialog.getOpenFileName()[0]
            self.updateText1(self.path)
        except:
            print(self.path)


    def updateText(self):
        random_text = np.random.randint(0, 100)
        self.label.setText("Your random number is %d" % random_text)
        self.label.adjustSize()
        # T[C] Ux[V]
        self.col1 = self.allData[self.columns[0]].to_numpy()
        self.col2 = self.allData[self.columns[2]].to_numpy()
        print(type(self.col1))
        print(type(self.col2))
        # T_A[K] T_B[K] CNT sr860x[V] sr860y[V] sr860f[Hz] sr860sin[V]
        self.graphWidget.plot(self.col1, self.col2)

    def updateText1(self, string):
        self.label.setText("Your file: %s" % string)
        self.label.adjustSize()

    def dataLoad(self):
        self.allData = pd.read_csv(self.path, delimiter=' ')
        if self.allData.size == 0:
            return
        self.allData.fillna('', inplace=True)
        self.columns = self.allData.columns.tolist()
        print(self.columns)

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

        QTimer.singleShot(5000, self.dataLoad)
        print('reading all data')

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

        self.showButton = QPushButton("&Show")
        self.showButton.clicked.connect(self.dataLoad)

        self.testButton = QPushButton("&Plot")
        self.testButton.clicked.connect(self.updateText)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(self.readButton)
        layout.addWidget(self.showButton)
        layout.addWidget(self.testButton)
        layout.addWidget(self.label)
        layout.addWidget(self.tableWidget)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Resulting chart:")

        checkBox = QCheckBox("test")

        self.x = list(range(100))  # 100 time points
        self.y = [np.random.randint(0, 100) for _ in range(100)]  # 100 data points
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        # pen = pg.mkPen(color=(255, 0, 0))
        # self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)


        layout = QHBoxLayout()
        layout.addWidget(checkBox)
        layout.addWidget(self.graphWidget)
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
        