from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolBar, QStatusBar, QMainWindow, QFileDialog, QTableWidgetItem)
from PyQt6.QtGui import QIcon, QAction
import pandas as pd
import random
import time


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

    def updateTextTable(self, string):
        self.label.setText("Your file: %s" % string) 
        self.label.adjustSize()

    def dataLoad(self):
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
            print("Loaded: ")
            #Rekurencyjne wykonywanie funkcji
            QTimer.singleShot(5000, self.afterFileIsLoaded(all_data))
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
        QTimer.singleShot(5000, self.afterFileIsLoaded(all_data))
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

        self.testButton = QPushButton("&Stop")
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

        layout = QHBoxLayout()
        layout.addWidget(checkBox)
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
        