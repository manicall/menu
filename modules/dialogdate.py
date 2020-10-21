# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import datetime as dt


class DialogDate(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.first_date = None
        self.last_date = None
        self.setWindowTitle("Выбрать диапазон")
        self.resize(250, 70)

        # dataTimeEdit=======================================
        #dt = datetime.datetime.today()\
        delta = dt.timedelta(days=365)
        dt_min = dt.date(dt.date.today().year, 1, 1)
        dt_max = dt.date(dt.date.today().year, 12, 31)
        self.dateTimeEdit1 = QtWidgets.QDateEdit(dt.date(dt.date.today().year, 1, 1))
        self.dateTimeEdit2 = QtWidgets.QDateEdit(dt.date(dt.date.today().year, 12, 31))
        self.dateTimeEdit1.setDateRange(dt_min, dt_max)
        self.dateTimeEdit1.setCalendarPopup(True)
        self.dateTimeEdit2.setDateRange(dt_min, dt_max)
        self.dateTimeEdit2.setCalendarPopup(True)
        button = QtWidgets.QPushButton("Ввести")
        button.clicked.connect(self.on_clicked)
        button.clicked.connect(self.accept)

        # grid================================================
        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel('Дата начала:'), 0, 0)
        grid.addWidget(QtWidgets.QLabel('Дата конца:'), 1, 0)
        grid.addWidget(self.dateTimeEdit1, 0, 1)
        grid.addWidget(self.dateTimeEdit2, 1, 1)

        # box===========================
        box = QtWidgets.QVBoxLayout()
        box.addLayout(grid)
        box.addWidget(button)
        self.setLayout(box)

    def on_clicked(self):
        if self.dateTimeEdit1.date() <= self.dateTimeEdit2.date():
            self.first_date = self.dateTimeEdit1.date().toPyDate()
            self.last_date = self.dateTimeEdit2.date().toPyDate()
        else:
            self.first_date = self.dateTimeEdit2.date().toPyDate()
            self.last_date = self.dateTimeEdit1.date().toPyDate()
        self.close()
