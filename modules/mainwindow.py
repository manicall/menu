from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from modules.widget import Widget
from modules.mydate import myDate
import pickle

colors = [
'#000000',
'#808080',
'#C0C0C0',
'#FFFFFF',
'#FF00FF',
'#800080',
'#FF0000',
'#800000',
'#FFFF00',
'#808000',
'#00FF00',
'#008000',
'#00FFFF',
'#008080',
'#0000FF',
'#000080'
]

class MainWindow(QtWidgets.QMainWindow):
    """
    Заполнение меню и строки инструментов элементами;
    привязка действий изображений и горячих клавиш к элементам
    Связывание меню и строки инструментов со строкой состояния.
    Создание постоянного сообщения на строке состояния.
    """

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)

        self.printer = QtPrintSupport.QPrinter()
        self.widget = Widget()
        self.setCentralWidget(self.widget)
        self.settings = QtCore.QSettings("max", "menu")
        self.fileName = self.settings.value('fileName')
        self.current_color_index = None
        menuBar = self.menuBar()
        toolBar = QtWidgets.QToolBar()
        # первое меню=========================================================
        myMenuFile = menuBar.addMenu("&Файл")
        action = myMenuFile.addAction(QtGui.QIcon(r"images/new.png"),
                                      "&Новый", self.widget.clear_all_cells,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_N
                                      )
        toolBar.addAction(action)
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
                                      "Сохранить &как...", self.save_as,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        toolBar.addAction(action)
        action.setStatusTip("Выбрать файл для сохранения")

        myMenuFile.addSeparator()
        action = myMenuFile.addAction("&Выход", QtWidgets.qApp.quit,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        action.setStatusTip("Завершение работы приложения")
        toolBar.addSeparator()
        # третье меню===============================================
        myMenuModel = menuBar.addMenu("&Модель таблицы")
        action = myMenuModel.addAction("По умолчанию", self.widget.table.show_default_table)
        action.setStatusTip("7 дней от текущего дня")
        myMenuModel.addSeparator()

        action = myMenuModel.addAction("Неделя", self.widget.table.show_week_table)
        action.setStatusTip("Выбрать неделю")

        action = myMenuModel.addAction("Месяц", self.widget.table.show_month_table)
        action.setStatusTip("Выбрать месяц")

        action = myMenuModel.addAction("На семестр", self.widget.table.show_semestr_table)
        action.setStatusTip("Показать таблицу по всему семестру")

        # toolbar_colors==========================================
        self.buttons = [QtWidgets.QPushButton() for i in range(len(colors))]  # генератор
        for i in range(len(self.buttons)):
            self.buttons[i].setFixedSize(22, 20)
            self.buttons[i].setStyleSheet('background-color:' + colors[i] +  '; margin-left: 2px;')
            self.buttons[i].clicked.connect(lambda event, index=i: self.choose_color(index))
            toolBar.addWidget(self.buttons[i])
        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)


        # строка состояния=======================================
        myD = myDate()
        self.label1 = QtWidgets.QLabel("дней до конца семестра: " + str(myD.days_left) + " ")
        self.label1.setMinimumSize(160, 20)
        self.label2 = QtWidgets.QLabel("текущая неделя: " + str(myD.this_week) + " ")
        self.label2.setMinimumSize(160, 20)
        status_bar = self.statusBar()
        status_bar.setSizeGripEnabled(False)
        status_bar.addPermanentWidget(self.label1)
        status_bar.addPermanentWidget(self.label2)



    # сохранение информации о таблице в двоичный файл
    def save(self):
        if not self.settings.contains('fileName'):
            self.fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         "Выберите файл", self.fileName,
                                                         "Файл (*.bin)")[0]
            self.settings.setValue('fileName', self.fileName)
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

    def choose_color(self, i):
        if self.current_color_index != None:
            self.buttons[self.current_color_index].setStyleSheet(
                'background-color:' + colors[self.current_color_index] + '; margin-left: 2px;')
        self.current_color_index = i
        self.buttons[i].setStyleSheet(
            'background-color:' + colors[i] + '; margin-left: 2px; border: 3px solid DarkSeaGreen;')



