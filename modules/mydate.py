from time import localtime
from datetime import date
import calendar
DAYSINWEEK = 7

class myDate:
    def __init__(self):
        self.time = localtime()
        self.d = ["понедельник", "вторник", "среда", "четверг",
                  "пятница", "суббота", "воскресенье"]
        #зависят от семестра
        self.first_date = date(self.time.tm_year, 9, 1)
        self.last_date = date(self.time.tm_year, 12, 21)
        self.days_left = self.last_date - date.today()
        self.days_past = date.today() - self.first_date
        self.total_date = self.last_date - self.first_date
        # 7 - количество дней в неделе
        self.this_week = (self.days_past.days + calendar.monthrange(2020, 9)[0] + 7) // 7

    def standart_module_dates(self):
        full_dates = []
        for col in range(1, 8):
            day = str(self.time.tm_mday + col - 1)
            month = str(self.time.tm_mon)
            weekday_index = self.time.tm_wday + col - 1 \
                if self.time.tm_wday + col < DAYSINWEEK else self.time.tm_wday + col - DAYSINWEEK - 1
            day_of_week = self.d[weekday_index]
            full_dates.append(day + '.' + month + '\n' + day_of_week)
        return full_dates

    def week_module_dates(self):
        full_dates = []
        for col in range(7):
            day = str(self.time.tm_mday + col)
            month = str(self.time.tm_mon)
            weekday_index = self.time.tm_wday + col \
                if self.time.tm_wday + col < DAYSINWEEK else self.time.tm_wday + col - DAYSINWEEK
            day_of_week = self.d[weekday_index]
            full_dates.append(day + '.' + month + '\n' + day_of_week)
        return full_dates

    def month_model(self):
        pass

    def semestr_model(self):
        full_dates = []
        for col in range(self.total_date.days):
            pass


