from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mydate import myDate
import copy

class Models:
    def __init__(self):
        self.myD = myDate()
        self.semestr_model = QtGui.QStandardItemModel(10, self.myD.total_date.days)
        self.semestr_model.setHorizontalHeaderLabels(list("{0:112}".format("")))
        self.semestr_model.setHorizontalHeaderLabels(["Время"])
        self.semestr_model.setVerticalHeaderLabels(list("{0:10}".format("")))
        self.semestr_model.setVerticalHeaderLabels(["Дата"])
        full_date = self.myD.semestr_model_dates()
        for col in range(self.myD.total_date.days):
            self.semestr_model.setItem(0, col + 1, self.get_item(full_date[col]))
        self.semestr_model.setItem(0, 0, self.get_item(''))

    def standart_model(self):
        model = self.semestr_model
        #model.removeColumns(1, 104)
        print(model is self.semestr_model)
        full_date = self.myD.standart_model_dates()
        for col in range(7):
            model.setItem(0, col + 1, self.get_item("{0:^10}".format(full_date[col])))
        model.setItem(0, 0, self.get_item(''))
        return model

    def week_model(self):

        model = QtGui.QStandardItemModel(10, 8)
        model.setHorizontalHeaderLabels(list("{0:8}".format("")))
        model.setHorizontalHeaderLabels(["Дисциплина"])
        model.setVerticalHeaderLabels(list("{0:10}".format("")))
        model.setVerticalHeaderLabels(["Дата"])

        weeks = []
        for i in range(16): weeks.append('неделя ' + str(i + 1))
        s, ok = QtWidgets.QInputDialog.getItem(None, "Выбор недели",
                                               "Выбрать неделю", weeks,
                                               current=self.myD.this_week - 1)

    def month_model(self):
        pass



    @staticmethod
    def get_item(str):
        item = QtGui.QStandardItem(str)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setEditable(False)
        item.setSelectable(False)
        return item

class Table:
    def __init__(self):
        self.models = Models()
        self.view = QtWidgets.QTableView()
        self.set_standart_model()
        self.view.resizeRowToContents(0)

    def set_standart_model(self):
        self.view.setModel(self.models.standart_model())
        self.hideColumns(self.view, 8, 104)

    def set_week_model(self):
        self.view.setModel(self.models.week_model())

    def set_month_model(self):
        self.view.setModel(self.models.month_model())

    def set_semestr_model(self):
        self.view.setModel(self.models.semestr_model)
        self.showAllColumns()

    def hideColumns(self, view, col, count):
        for i in range(count):
            view.hideColumn(col+i)

    def showAllColumns(self, view):
        for i in view.c:
            column.showColumn()


