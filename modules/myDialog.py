# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
import os


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent, flags=QtCore.Qt.Popup)
        self.setWindowTitle("Диалоговое окно")
        self.grid = QtWidgets.QGridLayout()
        self.buttons = [[]]
        self.paths = []
        self.choosen_path = None
        i = 0
        j = 0
        for entry in os.scandir('icons'):
            if j == 7:
                self.buttons.append([])
                i += 1
                j = 0
            self.buttons[i].append(QtWidgets.QPushButton(icon=QtGui.QIcon(entry.path)))
            self.paths.append(entry.path)
            j += 1
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.buttons[i][j].setFixedWidth(25)
                self.buttons[i][j].clicked.connect(lambda event, index=i+j: self.ChooseIcon(index))

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.grid.addWidget(self.buttons[i][j], i, j)
        self.setLayout(self.grid)

    def ChooseIcon(self, i):
        self.choosen_path = self.paths[i]
        self.close()
