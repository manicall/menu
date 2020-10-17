from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from modules.widget import Widget
from modules.mydate import myDate
import pandas as pd


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
                                      "&Открыть...", self.read_from_excel,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        toolBar.addAction(action)
        action.setStatusTip("Загрузка из файла")
        action = myMenuFile.addAction(QtGui.QIcon(r"images/save.png"),
                                      "Со&хранить...", self.save_to_excel,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        toolBar.addAction(action)
        action.setStatusTip("Сохранение в текущем файле")
        action = myMenuFile.addAction(QtGui.QIcon(r"images/save as.png"),
                                      "Сохранить &как...", self.save_to_excel_as,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        toolBar.addAction(action)
        action.setStatusTip("Выбрать файл для сохранения")


        myMenuFile.addSeparator()
        action = myMenuFile.addAction("&Выход", QtWidgets.qApp.quit,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        action.setStatusTip("Завершение работы приложения")

        # второе меню=========================================================
        myMenuEdit = menuBar.addMenu('&Редактировать')
        action = myMenuEdit.addAction("&Объединить", self.widget.span_cells)
        action.setStatusTip("Объединить выбранные ячейки")

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

        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)
        # строка состояния=======================================
        myD = myDate()
        self.label = QtWidgets.QLabel("дней до конца семестра: " + str(myD.days_left) + " ")
        self.label.setMinimumSize(160, 20)
        self.label1 = QtWidgets.QLabel("текущая неделя: " + str(myD.this_week) + " ")
        self.label1.setMinimumSize(160, 20)
        status_bar = self.statusBar()
        status_bar.setSizeGripEnabled(False)
        status_bar.addPermanentWidget(self.label)
        status_bar.addPermanentWidget(self.label1)

    def save_to_excel(self):
        if not self.settings.contains('fileName'):
            self.fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         "Выберите файл", self.fileName,
                                                         "Excel (*.xlsx)")[0]
            self.settings.setValue('fileName', self.fileName)
        if self.fileName:
            model = self.widget.table.model
            values = []
            for i in range(0, model.rowCount()):
                values.append([])
                for j in range(0, model.columnCount()):
                    try:
                        values[i].append(model.item(i, j).text())
                    except:
                        values[i].append("")
            df = pd.DataFrame(values)
            df.to_excel(self.fileName, index=False, header=False)

    def read_from_excel(self):
        self.fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "Выберите файл", self.fileName,
                                                         "Excel (*.xlsx)")[0]
        if self.fileName:
            self.settings.setValue('fileName', self.fileName)
            model = self.widget.table.model
            df = pd.read_excel(self.fileName, index_col=None, header=None)

            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    item = QtGui.QStandardItem(str(df[j][i]))
                    if item.text() != 'nan':
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        model.setItem(i, j, item)
            for i in range(model.rowCount()):
                self.widget.table.view.resizeRowToContents(i)

    def save_to_excel_as(self):
        self.fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              "Выберите файл", self.fileName,
                                                              "Excel (*.xlsx)")[0]
        if self.fileName:
            self.settings.setValue('fileName', self.fileName)
            model = self.widget.table.model
            '''
            values = []
            for i in range(0, model.rowCount()):
                values.append([])
                for j in range(0, model.columnCount()):
                    try:
                        values[i].append(model.item(i, j).text())
                    except:
                        values[i].append("")
            df = pd.DataFrame(values)
            df.to_excel(self.fileName, index=False, header=False)
            '''


