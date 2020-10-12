import datetime as dt
import calendar
import locale

class myDate:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")
        self.WEEK = 7
        #зависят от семестра
        self.first_date = dt.date(dt.date.today().year, 9, 1)
        self.last_date = dt.date(dt.date.today().year, 12, 21)
        #===================
        self.days_left = (self.last_date - dt.date.today()).days
        self.days_past = (dt.date.today() - self.first_date).days
        self.total_days = (self.last_date - self.first_date).days
        self.total_weeks = (self.total_days + self.WEEK) // self.WEEK
        self.this_week = (self.days_past + calendar.monthrange(2020, 9)[0] + self.WEEK) // self.WEEK

    def model_dates(self):
        full_dates = []
        for col in range(self.total_days):
            date = self.first_date + dt.timedelta(col)
            day = date.day
            month = date.month
            day_of_week = calendar.day_name[date.weekday()]
            full_dates.append(str(day) + '.' + str(month) + '\n' + day_of_week)
        return full_dates


