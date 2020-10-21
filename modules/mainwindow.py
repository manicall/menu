from PyQt5 import QtCore, QtGui, QtWidgets
from modules.widget import Widget, colors
from modules.mydate import myDate
import pickle
import os


class MainWindow(QtWidgets.QMainWindow):
    """
    Заполнение меню и строки инструментов элементами;
    привязка действий изображений и горячих клавиш к элементам
    Связывание меню и строки инструментов со строкой состояния.
    Создание постоянного сообщения на строке состояния.
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        self.settings = QtCore.QSettings("config.ini", QtCore.QSettings.IniFormat)
        # для отладки
        self.fileName = self.settings.value('fileName')
        self.widget = Widget()
        self.setCentralWidget(self.widget)
        menuBar = self.menuBar()
        toolBar = QtWidgets.QToolBar()

        # первое меню=========================================================
        myMenuFile = menuBar.addMenu("&Файл")
        action = myMenuFile.addAction(QtGui.QIcon(r"images/new.png"),
                                      "&Новый", self.clear_all_cells,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_N
                                      )
        action.setStatusTip("Создание нового файла")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/open.png"),
                                      "&Открыть...", self.read,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        toolBar.addAction(action)
        action.setStatusTip("Загрузка из файла")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/save.png"),
                                      "Со&хранить...", self.save,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        toolBar.addAction(action)
        action.setStatusTip("Сохранение в текущем файле")
        action = myMenuFile.addAction(QtGui.QIcon(r"images/save as.png"),
                                      "Сохранить &как...", self.save_as)
        action.setStatusTip("Выбрать файл для сохранения")

        myMenuFile.addSeparator()
        action = myMenuFile.addAction("&Выход", QtWidgets.qApp.quit,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        action.setStatusTip("Завершение работы приложения")
        toolBar.addSeparator()

        # Второе меню===============================================
        menuBar = self.menuBar()
        self.myMenuModel = menuBar.addMenu("&Модель таблицы")
        action = self.myMenuModel.addAction("По умолчанию", self.widget.table.show_default_table)
        action.setStatusTip("7 дней от текущего дня")
        self.myMenuModel.addSeparator()
        action = self.myMenuModel.addAction("Неделя", self.widget.table.show_week_table)
        action.setStatusTip("Выбрать неделю")
        action = self.myMenuModel.addAction("Месяц", self.widget.table.show_month_table)
        action.setStatusTip("Выбрать месяц")
        action = self.myMenuModel.addAction("На семестр", self.widget.table.show_semestr_table)
        action.setStatusTip("Показать таблицу по всему семестру")

        # toolbar_colors==========================================
        self.buttons = [QtWidgets.QPushButton() for i in range(len(colors))]  # генератор
        for i in range(len(self.buttons)):
            self.buttons[i].setFixedSize(22, 20)
            self.buttons[i].move(100, 100)
            self.buttons[i].setStyleSheet('background-color:' + colors[i] + '; margin-left: 2px;')
            self.buttons[i].clicked.connect(lambda event, index=i: self.choose_color(index))
            toolBar.addWidget(self.buttons[i])
        toolBar.addSeparator()
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["Установить цвет ячейки", "Установить цвет шрифта"])
        toolBar.addWidget(self.comboBox)
        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)

        # строка состояния=======================================
        self.myD = myDate()
        self.label1 = QtWidgets.QLabel("дней до конца семестра: " + str(self.myD.days_left) + " ")
        self.label1.setMinimumSize(160, 20)
        self.label2 = QtWidgets.QLabel("текущая неделя: " + str(self.myD.this_week) + " ")
        self.label2.setMinimumSize(160, 20)
        self.status_bar = self.statusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.addPermanentWidget(self.label1)
        self.status_bar.addPermanentWidget(self.label2)

    # сохранение информации о таблице в двоичный файл
    def save(self):
        if not self.settings.contains('fileName'):
            self.fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                  "Выберите файл", self.fileName,
                                                                  "Файл (*.bin)")[0]
        if self.fileName:
            self.settings.setValue('fileName', self.fileName)
            print(self.fileName)
            file = open(self.fileName, "wb")
            pickle.dump(self.widget.table.model_for_save, file)
            file.close()

    # открытие информации о таблице
    def read(self):
        self.fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                                                              "Выберите файл", self.fileName,
                                                              "Файл (*.bin)")[0]
        if self.fileName:
            self.settings.setValue('fileName', self.fileName)
            file = open(self.fileName, "rb")
            model_for_save = pickle.load(file)
            file.close()
            self.widget.table.input_opened_model(model_for_save)

    # открыть раннее сохраненный файл
    def open_early_file(self):
        if self.settings.contains('fileName'):
            file = open(self.fileName, "rb")
            model_for_save = pickle.load(file)
            file.close()
            self.widget.table.input_opened_model(model_for_save)

    # обязательный выбор файла при сохранении
    def save_as(self):
        self.fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              "Выберите файл", self.fileName,
                                                              "Файл (*.bin)")[0]
        if self.fileName:
            self.settings.setValue('fileName', self.fileName)
            print(self.fileName)
            file = open(self.fileName, "wb")
            pickle.dump(self.widget.table.model_for_save, file)
            file.close()

    # выбор цвета из меню на toolbar
    def choose_color(self, i):
        if self.comboBox.currentText() == "Установить цвет ячейки":
            self.widget.set_cell_color(i)
        if self.comboBox.currentText() == "Установить цвет шрифта":
            self.widget.set_font_color(i)


    def clear_all_cells(self):
        # удаление сохраненного имени файла,
        # чтобы пользователь случайно не стер сохраненный ранее файл
        self.settings.remove('fileName')
        self.settings.remove('firstDate')
        self.settings.remove('lastDate')
        self.settings.sync()
        self.close()
        # рекомендуется не менять название главного модуля
        os.system('py main.pyw')
