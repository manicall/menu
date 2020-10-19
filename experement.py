# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
import sys
import os

class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Диалоговое окно")
        self.resize(200, 70)
        self.mainBox = QtWidgets.QVBoxLayout()
        self.buttons = []

        for entry in os.scandir('icons'):
            self.buttons.append(QtWidgets.QPushButton(icon= QtGui.QIcon(entry.path)))
        for i in range(len(self.buttons)):
            try:
                self.buttons[i].clicked.connect(lambda: self.ChooseIcon(i))
            except: print(sys.exc_info())
            self.mainBox.addWidget(self.buttons[i])

        self.setLayout(self.mainBox)

    def ChooseIcon(self, i):
        print(i)


def on_clicked():
    dialog = MyDialog(window)
    dialog.exec_()


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Класс QDialog")
window.resize(300, 70)

button = QtWidgets.QPushButton("Отобразить диалоговое окно...")
button.clicked.connect(on_clicked)

box = QtWidgets.QVBoxLayout()
box.addWidget(button)
window.setLayout(box)

window.show()
sys.exit(app.exec_())
