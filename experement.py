# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
import sys


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.label = QtWidgets.QLabel("Содержимое страницы")
        self.button = QtWidgets.QPushButton("Кнопка")
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(self.label)
        self.box.addWidget(self.button)
        self.setLayout(self.box)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.w = MyWidget()
        self.setCentralWidget(self.w)
        self.w.button.clicked.connect(self.on_clicked)
        # self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QtCore.QSize(32, 32))
        # self.setAnimated(False)
        self.add_menu()
        self.add_tool_bar()

    def add_menu(self):
        self.menuFile = QtWidgets.QMenu("&File")
        self.actOpen = QtWidgets.QAction("Open", None)
        ico = self.style().standardIcon(
            QtWidgets.QStyle.SP_ComputerIcon)
        self.actOpen.setIcon(ico)
        self.actOpen.setShortcut(QtGui.QKeySequence.Open)
        self.actOpen.triggered.connect(self.on_open)
        self.menuFile.addAction(self.actOpen)
        self.menuBar().addMenu(self.menuFile)

    def add_tool_bar(self):
        self.toolBar = QtWidgets.QToolBar("MyToolBar")
        self.toolBar.addAction(self.actOpen)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)

        self.toolBar2 = QtWidgets.QToolBar("MyToolBar2")
        ico = self.style().standardIcon(
            QtWidgets.QStyle.SP_DialogCloseButton)
        self.actQuit = self.toolBar2.addAction(ico, "Quit",
                                               QtWidgets.qApp.quit)
        self.actQuit.setShortcut(QtGui.QKeySequence.Quit)
        self.toolBar2.setAllowedAreas(QtCore.Qt.TopToolBarArea |
                                      QtCore.Qt.BottomToolBarArea)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar2)

    def on_open(self):
        print("Выбран пункт меню Open")

    def on_clicked(self):
        pass


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.setWindowTitle("Класс QToolBar")
window.resize(500, 350)

window.show()
sys.exit(app.exec_())
