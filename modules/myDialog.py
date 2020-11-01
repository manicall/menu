# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from modules.colors import colors
import os

class Icon:
    def out_icons(self):
        self.grid = QtWidgets.QGridLayout()
        self.buttons = [[]]
        self.paths = []
        self.choosen_path = None
        i = 0
        j = 0
        # заполняет список кнопками с иконками
        for entry in os.scandir('icons'):
            if j == 7:
                self.buttons.append([])
                i += 1
                j = 0
            self.buttons[i].append(QtWidgets.QPushButton(icon=QtGui.QIcon(entry.path)))
            self.paths.append(entry.path)
            j += 1
        # изменяет размеры кнопок и соединяет с обрабатывающей функцией
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.buttons[i][j].setFixedWidth(25)
                self.buttons[i][j].clicked.connect(lambda event, index=i + j: self.ChooseIcon(index))
        # добавляет кнопки в слой
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.grid.addWidget(self.buttons[i][j], i, j)
        self.setLayout(self.grid)

    def ChooseIcon(self, i):
        self.choosen_path = self.paths[i]  # запомнить выбор иконки
        self.close()

class Color:
    def out_colors(self, mainWindow):
        self.grid = QtWidgets.QGridLayout()
        self.buttons = [QtWidgets.QPushButton() for i in range(len(colors))]  # генератор
        for i in range(len(self.buttons)):
            self.buttons[i].setFixedSize(22, 20)
            self.buttons[i].move(100, 100)
            self.buttons[i].setStyleSheet('background-color:' + colors[i] + '; margin-left: 2px;')
            self.buttons[i].clicked.connect(lambda event, dialog=self, index=i: mainWindow.choose_color(index, dialog))
            self.grid.addWidget(self.buttons[i], 0, i)
        self.setLayout(self.grid)


class MyDialog(QtWidgets.QDialog, Icon):
    # перед вызовом методов примесей следует вызвать конструктор
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent, flags=QtCore.Qt.Popup)

    def out_icons(self):
        Icon.out_icons(self)
        self.move(QtGui.QCursor.pos())
        self.exec()

    def out_colors(self, mainWindow):
        Color.out_colors(self, mainWindow)
        self.move(QtGui.QCursor.pos())
        self.exec()
