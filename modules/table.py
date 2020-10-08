from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import date
from time import localtime
import calendar
DAYSINWEEK = 7


class Models:
    def __init__(self):
        self.d = ["понедельник", "вторник", "среда", "четверг",
                  "пятница", "суббота", "воскресенье"]
        self.standart_model = self.get_standart_model()  # расписание на неделю

    def get_standart_model(self):
        #grid = QtWidgets.QGridLayout()
        #grid.addWidget(QtWidgets.QTextEdit, 0, 0)
        #grid.addWidget(QtWidgets.QTextEdit, 0, 1)
        time = localtime()
        model = QtGui.QStandardItemModel(10, DAYSINWEEK + 1)
        model.setHorizontalHeaderLabels(list("{0:8}".format("")))
        model.setHorizontalHeaderLabels(["Дисциплина"])
        model.setVerticalHeaderLabels(list("{0:10}".format("")))
        model.setVerticalHeaderLabels(["Дата"])
        for col in range(1, 8):
            day = str(time.tm_mday + col - 1)
            month = str(time.tm_mon)
            weekday_index = time.tm_wday + col - 1 if time.tm_wday + col < DAYSINWEEK else time.tm_wday + col - DAYSINWEEK - 1
            day_of_week = self.d[weekday_index]
            full_date = day + '.' + month + '\n' + day_of_week
            model.setItem(0, col, self.get_item("{0:^10}".format(full_date)))
        model.setItem(0, 0, self.get_item(''))
        return model

    def this_week_model(self):
        pass

    def get_item(self, str):
        item = QtGui.QStandardItem(QtGui.QStandardItem(str))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setEditable(False)
        item.setSelectable(False)
        return item


class Table:
    def __init__(self):
        self.models = Models()
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.models.standart_model)
        self.view.resizeRowToContents(0)


    def change_model(self, model):
        self.view.setModel(self.standart_model)
