from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mydate import myDate
import pickle


class myItem:
    def __init__(self, text='', image='', font_color='#000000', background_color='#ffffff'):
        self.text = text
        self.image = image
        self.font_color = font_color
        self.background_color = background_color


class ModelForSave:
    def __init__(self, rows, cols):
        # инициализация модели
        self.rowCount = rows
        self.columnCount = cols
        self.model = [[myItem()]]
        self.model.pop()
        for i in range(rows):
            self.model.append([])
        for i in range(rows):
            for j in range(cols):
                self.model[i].append(None)


    def set_item(self, row, column, myItem):
        self.model[row].pop(column)
        self.model[row].insert(column, myItem)


class Models:
    def __init__(self):
        self.myD = myDate()
        full_date = self.myD.model_dates()
        self.model_for_save = ModelForSave(50, self.myD.total_days + 1)
        self.model = QtGui.QStandardItemModel(50, self.myD.total_days + 1)


        for col in range(self.myD.total_days):
            self.model.setItem(0, col + 1, self.get_item(full_date[col]))
            self.model_for_save.set_item(0, col + 1, myItem(full_date[col]))
        self.model.setItem(0, 0, self.get_item(''))
        self.set_data_roles()
        #print(self.model_for_save.model)


    @staticmethod
    def get_item(str):
        item = QtGui.QStandardItem(str)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setEditable(False)
        item.setSelectable(False)
        return item

    def set_data_roles(self):
        for i in range(1, self.model.rowCount()):
            for j in range(1, self.model.columnCount()):
                self.model.setData(self.model.index(i, j), '', role=QtCore.Qt.DecorationRole)
