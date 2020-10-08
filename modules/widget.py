from PyQt5 import QtCore, QtWidgets
from modules.table import table
from datetime import date
class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        vBoxMain = QtWidgets.QVBoxLayout()
        self.box = QtWidgets.QVBoxLayout()
        vBoxMain.addWidget(table().view)
        self.setLayout(vBoxMain)

    def onClearAllCells(self):
        pass
