# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import sys, datetime

def on_clicked():
    print(dateTimeEdit.time())

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Класс QDateEdit")
dateTimeEdit = QtWidgets.QTimeEdit(None)

button = QtWidgets.QPushButton("Получить значение")
button.clicked.connect(on_clicked)
box = QtWidgets.QVBoxLayout()
box.addWidget(dateTimeEdit)
box.addWidget(button)
window.setLayout(box)
window.show()
sys.exit(app.exec_())
