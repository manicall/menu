from PyQt5 import QtWidgets, QtCore
import datetime as dt
import calendar
import locale
from modules.dialogdate import DialogDate

class myDate:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")
        self.WEEK = 7
        #===================
        self.settings = QtCore.QSettings("config.ini", QtCore.QSettings.IniFormat)
        if not (self.settings.contains('firstDate') and self.settings.contains('lastDate')):
            dialog = DialogDate()
            result = dialog.exec()
            if result == QtWidgets.QDialog.Accepted:
                self.settings.setValue('firstDate', dialog.first_date)
                self.settings.setValue('lastDate', dialog.last_date)
            else:
                exit(0)
        #===================
        self.first_date = self.settings.value('firstDate')
        self.last_date = self.settings.value('lastDate')
        self.days_left = (self.last_date - dt.date.today()).days
        self.days_past = (dt.date.today() - self.first_date).days
        self.total_days = (self.last_date - self.first_date).days
        self.total_weeks = (self.total_days + self.WEEK) // self.WEEK
        self.this_week = (self.days_past + calendar.monthrange(2020, 9)[0] + self.WEEK) // self.WEEK
    # даты отображаемые в верхней строке таблицы
    def model_dates(self):
        full_dates = []
        for col in range(self.total_days):
            date = self.first_date + dt.timedelta(col)
            day = date.day
            month = date.month
            day_of_week = calendar.day_name[date.weekday()]
            full_dates.append(str(day) + '.' + str(month) + '\n' + day_of_week)
        return full_dates
