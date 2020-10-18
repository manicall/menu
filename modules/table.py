from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mydate import myDate
from modules.models import Models
import datetime as dt
import calendar
# размеры полной таблицы


class Table:
    def __init__(self):
        self.myD = myDate()
        self.model = Models().model
        self.model_for_save = Models().model_for_save
        self.model.dataChanged.connect(self.table_changed)
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        #self.view.horizontalHeader().hide()
        #self.view.verticalHeader().hide()
        self.show_default_table()
        self.view.resizeRowToContents(0)

    def show_default_table(self):
        self.showAllColumns()
        self.hideColumns(1, self.myD.days_past)
        self.hideColumns(self.myD.days_past + self.myD.WEEK + 1,
                         self.myD.days_left - self.myD.WEEK)

    def show_week_table(self):
        answer = self.choose_week()
        if(answer[1]):
            self.showAllColumns()
            number_of_week = int(answer[0].split()[1]) - 1
            weeks_before_last_date = self.myD.total_weeks - number_of_week
            self.showAllColumns()
            self.hideColumns(1, number_of_week*self.myD.WEEK - 1)
            self.hideColumns((number_of_week+1)*self.myD.WEEK, (weeks_before_last_date - 1)*self.myD.WEEK)

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
            while (i != self.myD.total_days + 1):
                self.view.hideColumn(i)
                i+=1

    def show_semestr_table(self):
        self.showAllColumns()

    def hideColumns(self, col, count):
        for i in range(count):
            self.view.hideColumn(col+i)

    def showAllColumns(self):
        for col in range(self.model.columnCount()):
            self.view.showColumn(col)

    def choose_week(self):
        weeks = []
        for i in range(self.myD.total_weeks):
            weeks.append('неделя ' + str(i + 1))
        answer = QtWidgets.QInputDialog.getItem(None, "Выбор недели",
                                                "Выбрать неделю", weeks,
                                                current=self.myD.this_week - 1, editable=False)
        return answer

    def choose_month(self):
        months = []
        for i in range(self.myD.first_date.month, self.myD.last_date.month + 1):
            months.append(calendar.month_name[i])
        answer = QtWidgets.QInputDialog.getItem(None, "Выбор недели",
                                                "Выбрать неделю", months,
                                                current=dt.date.today().month - self.myD.first_date.month,
                                                editable=False)
        for i in range(len(months)):
            if(months[i] == answer[0]):
                answer = (i + self.myD.first_date.month, answer[1])
        return answer

    def table_changed(self):
        self.view.resizeRowToContents(self.view.currentIndex().row())

