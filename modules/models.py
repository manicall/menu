from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mydate import myDate
from modules.ForSave.ForSave import ForSave, myItem

'''
Модель для отображения таблицы, которую видит пользователь.
'''
class Models:
    def __init__(self):
        rows_count = 50
        self.myD = myDate()
        full_date = self.myD.model_dates()
        # инициализация
        self.for_save = ForSave(rows_count, self.myD.total_days + 1)
        self.model = QtGui.QStandardItemModel(rows_count, self.myD.total_days + 1)
        # установка даты
        for col in range(self.myD.total_days):
            self.model.setItem(0, col + 1, self.get_item(full_date[col]))
            self.for_save.set_item(0, col + 1, myItem(full_date[col]))
        # заполнение ячеек пустым текстом, чтобы их можно было закрасить
        for i in range(1, rows_count):
            for j in range(1, self.myD.total_days):
                self.model.setItem(i, j, QtGui.QStandardItem(''))
        self.model.setItem(0, 0, self.get_item(''))
        # изменение заголовков
        self.model.setHorizontalHeaderLabels(['' for i in range(self.myD.total_days + 1)])
        self.model.setHorizontalHeaderItem(self.myD.days_past + 1, QtGui.QStandardItem("TODAY"))
        self.model.horizontalHeaderItem(self.myD.days_past + 1).setBackground(QtGui.QBrush(QtGui.QColor('black')))
        self.model.horizontalHeaderItem(self.myD.days_past + 1).setForeground(QtGui.QBrush(QtGui.QColor('white')))

    @staticmethod
    def get_item(str):
        item = QtGui.QStandardItem(str)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setEditable(False)
        item.setSelectable(False)
        return item
