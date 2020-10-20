from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mydate import myDate

'''
хранит информацию хранящуюся в ячейке
'''
class myItem:
    def __init__(self, text='', icon=None, font_color='#000000', background_color='#ffffff'):
        self.text = text
        self.icon = icon
        self.font_color = font_color
        self.background_color = background_color

'''
хранит информацию об объединенных ячейках
'''
class SpannedCells:
    def __init__(self, row=-1, column=-1, rowSpan=0, columnSpan=0):
        self.row = row
        self.column = column
        self.rowSpan = rowSpan
        self.columnSpan = columnSpan

'''
хранит информацию хранящуюся в таблице.
необходимо тк невозможно сохранять таблицу, 
которую видит пользователь
'''
class ModelForSave:
    def __init__(self, rows, cols):
        # инициализация модели
        self.rowCount = rows
        self.columnCount = cols
        self.spanned_cells = [SpannedCells()]
        self.model = [[myItem()]]
        # очистка контейнеров
        self.model.pop()
        self.spanned_cells.pop()
        for i in range(rows):
            self.model.append([])
        for i in range(rows):
            for j in range(cols):
                self.model[i].append(None)

    def set_item(self, row, column, myItem):
        if self.model[row][column] == None:
            self.model[row].pop(column)
            self.model[row].insert(column, myItem)
        else:
            if myItem.text != '':
                self.model[row][column].text = myItem.text
            if myItem.icon != None:
                self.model[row][column].icon = myItem.icon
            if myItem.font_color != '#000000':
                self.model[row][column].font_color = myItem.font_color
            if myItem.background_color != '#ffffff':
                self.model[row][column].background_color = myItem.background_color

    #def Clear(self):




'''
Модель для отображения таблицы, которую видит пользователь.
'''
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

    @staticmethod
    def get_item(str):
        item = QtGui.QStandardItem(str)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setEditable(False)
        item.setSelectable(False)
        return item
