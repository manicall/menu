from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mydate import myDate



class Models:
    def __init__(self):
        self.myD = myDate()

    def standart_model(self):
        model = QtGui.QStandardItemModel(10, 8)
        model.setHorizontalHeaderLabels(list("{0:8}".format("")))
        model.setHorizontalHeaderLabels(["Дисциплина"])
        model.setVerticalHeaderLabels(list("{0:10}".format("")))
        model.setVerticalHeaderLabels(["Дата"])
        full_date = self.myD.standart_module_dates()
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
        self.view.setModel(self.models.standart_model())
        self.view.resizeRowToContents(0)

    def change_model(self, model):
        self.view.setModel(model)

    def set_standart_model(self):
        self.change_model(self.models.standart_model())

    def set_week_model(self):
        self.change_model(self.models.week_model())

    def set_month_model(self):
        self.change_model(self.models.month_model())
