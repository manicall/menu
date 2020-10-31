from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mydate import myDate
from modules.models import Models
from modules.ForSave import ForSave
from modules.ForSave.ForSave import myItem, SpannedCells
import datetime as dt
import calendar
import sys


class Table:
    def __init__(self):
        self.changed = ForSave.changed
        self.myD = myDate()
        self.model = Models().model
        self.for_save = Models().for_save
        self.model.dataChanged.connect(self.onChange)
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        self.this_week()
        for i in range(self.model.columnCount()):
            self.view.setColumnWidth(i, 150)
        self.view.resizeRowToContents(0)


    def this_week(self):
        self.showAllColumns()
        number_of_week = int(self.myD.this_week) - 1
        weeks_before_last_date = self.myD.total_weeks - number_of_week
        self.showAllColumns()
        self.hideColumns(1, number_of_week * self.myD.WEEK - 1)
        self.hideColumns((number_of_week + 1) * self.myD.WEEK, (weeks_before_last_date - 1) * self.myD.WEEK)

    #расписание на выбранную неделю
    def show_week_table(self):
        answer = self.choose_week()
        if(answer[1]):
            self.showAllColumns()
            number_of_week = int(answer[0].split()[1]) - 1
            weeks_before_last_date = self.myD.total_weeks - number_of_week
            self.showAllColumns()
            self.hideColumns(1, number_of_week*self.myD.WEEK - 1)
            self.hideColumns((number_of_week+1)*self.myD.WEEK, (weeks_before_last_date - 1)*self.myD.WEEK)

    #расписание на выбранный месяц
    def show_month_table(self):
        answer = self.choose_month()
        if(answer[1]):
            self.showAllColumns()
            number_of_month = answer[0]
            month = calendar.monthrange(dt.date.today().year, number_of_month)
            i = 1
            while(self.model.item(0, i).text().split('\n')[0] != str(1) + '.' + str(number_of_month)):
                self.view.hideColumn(i)
                i+=1
            i += month[1]
            while (i <= self.myD.total_days + 1):
                self.view.hideColumn(i)
                i+=1

    # расписание на весь период
    def show_semestr_table(self):
        self.showAllColumns()

    def hideColumns(self, col, count):
        for i in range(count):
            self.view.hideColumn(col+i)

    def showAllColumns(self):
        for col in range(self.model.columnCount()):
            self.view.showColumn(col)

    def create_dialog(self, icon, title, text, items, current):
        dialog = QtWidgets.QInputDialog(None)
        dialog.setWindowIcon(icon)
        dialog.setWindowTitle(title)
        dialog.setLabelText(text)
        dialog.setComboBoxItems(items)
        dialog.setTextValue(items[current])
        dialog.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.WindowCloseButtonHint)
        dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        return dialog

    # выбор недели
    def choose_week(self):
        weeks = ['неделя ' + str(i + 1) for i in range(self.myD.total_weeks)]
        dialog = self.create_dialog(QtGui.QIcon('images/Week.png'), 'EEK', 'Выбрать неделю', weeks,
                                    current=self.myD.this_week - 1)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            answer = dialog.textValue(), True
        else:
            answer = dialog.textValue(), False
        return answer

    # выбор месяца
    def choose_month(self):
        months = [calendar.month_name[i] for i in range(self.myD.first_date.month, self.myD.last_date.month + 1)]
        dialog = self.create_dialog(QtGui.QIcon('images/Month.png'), "ONTH", "Выбрать неделю", months,
                                    current=dt.date.today().month - self.myD.first_date.month)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            answer = dialog.textValue(), True
        else:
            answer = dialog.textValue(), False
        for i in range(len(months)):
            print(months[i], answer[0])
            if (months[i] == answer[0]):
                answer = (i + self.myD.first_date.month, answer[1])
        return answer

    # если меняется содержимое ячейки
    def onChange(self):
        self.changed = True
        row, column = self.view.currentIndex().row(), self.view.currentIndex().column()
        if row != -1:
            self.view.resizeRowToContents(row)
            try:
                if self.for_save.model[row][column] != None:
                    self.for_save.model[row][column].text = self.model.item(row, column).text()
                else:
                    self.for_save.model.set_item(row, column, myItem(self.model.item(row, column).text()))
            except: print(sys.exc_info(), row, column)

        self.view.resizeRowsToContents()

    # изменение отображаемой таблицы в соответствии с информацией
    # хранящейся в двоичных файлах
    def input_opened_model(self, from_save):
        from_save.model.set_size(from_save.model.rowCount, from_save.model.columnCount)
        # устанавливает объединения
        for i in from_save.spanned_cells:
            self.for_save.spanned_cells.append(SpannedCells(i.row, i.column, i.rowSpan, i.columnSpan))
            self.view.setSpan(i.row, i.column, i.rowSpan, i.columnSpan)
        # устанавливает атрибуты ячеек
        for i in range(from_save.model.rowCount):
            for j in range(from_save.model.columnCount):
                if from_save.model[i][j] != None:
                    # установка иконки
                    self.model.setData(self.model.index(i, j),
                                       QtGui.QIcon(from_save.model[i][j].icon),
                                       role=QtCore.Qt.DecorationRole)
                    # установка текста
                    self.model.item(i, j).setText(from_save.model[i][j].text)
                    # установка цвета ячейки
                    self.model.item(i, j).setBackground(
                        QtGui.QBrush(QtGui.QColor(from_save.model[i][j].background_color)))
                    # установка цвета шрифта
                    self.model.item(i, j).setForeground(
                        QtGui.QBrush(QtGui.QColor(from_save.model[i][j].font_color)))
                    # сохранение атрибутов в модели для сохранения
                    self.for_save.model.set_item(i, j, from_save.model[i][j])
        self.view.resizeRowsToContents()