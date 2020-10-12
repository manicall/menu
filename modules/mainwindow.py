from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
import re
from modules.widget import Widget
from modules.mydate import myDate


class MainWindow(QtWidgets.QMainWindow):
    """
    Заполнение меню и строки инструментов элементами;
    привязка действий изображений и горячих клавиш к элементам
    Связывание меню и строки инструментов со строкой состояния.
    Создание постоянного сообщения на строке состояния.
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent,
                                       flags=QtCore.Qt.Window |
                                             QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.printer = QtPrintSupport.QPrinter()
        self.widget = Widget()
        self.setCentralWidget(self.widget)
        menuBar = self.menuBar()
        toolBar = QtWidgets.QToolBar()
        #=========================первое меню
        myMenuFile = menuBar.addMenu("&Файл")
        action = myMenuFile.addAction(QtGui.QIcon(r"images/new.png"),
            "&Новый", self.widget.onClearAllCells,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_N
                                      )
        toolBar.addAction(action)
        action.setStatusTip("Создание нового файла")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/open.png"),
                                      "&Открыть...", self.onOpenFile,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        toolBar.addAction(action)
        action.setStatusTip("Загрузка из файла")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/save.png"),
                                      "Со&хранить...", self.onSave,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        toolBar.addAction(action)
        action.setStatusTip("Сохранение в файле")

        myMenuFile.addSeparator()
        toolBar.addSeparator()
        action = myMenuFile.addAction("&Выход", QtWidgets.qApp.quit,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        action.setStatusTip("Завершение работы приложения")
        #===========================второе меню
        myMenuEdit = menuBar.addMenu("&Правка")
        action = myMenuEdit.addAction(QtGui.QIcon(r"images/copy.png"),
                                      "К&опировать", self.onCopyData,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_C)
        toolBar.addAction(action)
        action.setStatusTip("Копирование в буфер обмена")
        action = myMenuEdit.addAction("Копировать &для Excel",
                                      self.onCopyDataExcel)
        action.setStatusTip("Копирование в формате MS Excel")
        action = myMenuEdit.addAction(QtGui.QIcon(r"images/paste.png"),
                                      "&Вставить", self.onPasteData,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_V)
        toolBar.addAction(action)
        action.setStatusTip("Вставка головоломки из буфера обмена")
        action = myMenuEdit.addAction("Вставить &из Excel",
                                      self.onPasteDataExcel)
        action.setStatusTip("Вставка головоломки из MS Excel")

        myMenuEdit.addSeparator()
        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)
        #===========================третье меню
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
        #====================строка состояния
        myD = myDate()
        self.label = QtWidgets.QLabel("дней до конца семестра: " + str(myD.days_left) + " ")
        self.label.setMinimumSize(160, 20)
        self.label1 = QtWidgets.QLabel("текущая неделя: " + str(myD.this_week) + " ")
        self.label1.setMinimumSize(160, 20)
        status_bar = self.statusBar()
        status_bar.setSizeGripEnabled(False)
        status_bar.addPermanentWidget(self.label)
        status_bar.addPermanentWidget(self.label1)

    def onCopyData(self):
        QtWidgets.QApplication.clipboard().setText(
            self.widget.getDataAllCells())

    def onCopyDataMini(self):
        QtWidgets.QApplication.clipboard().setText(
            self.widget.getDataAllCellsMini())

    def onCopyDataExcel(self):
        QtWidgets.QApplication.clipboard().setText(
            self.widget.getDataAllCellsExcel())

    def onPasteData(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            if len(data) == 81 or len(data) == 162:
                r = re.compile(r"[^0-9]")
                if not r.match(data):
                    self.widget.setDataAllCells(data)
                    return
        self.dataErrorMsg()

    def onPasteDataExcel(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            data = data.replace("\r", "")
            r = re.compile(r"([0-9]?[\t\n]){81}")
            if r.match(data):
                result = []
                if data[-1] == "\n":
                    data = data[:-1]
                dl = data.split("\n")
                for sl in dl:
                    dli = sl.split("\t")
                    for sli in dli:
                        if len(sli) == 0:
                            result.append("00")
                        else:
                            result.append("0" + sli[0])
                data = "".join(result)
                self.widget.setDataAllCells(data)
                return
        self.dataErrorMsg()

    def dataErrorMsg(self):
        QtWidgets.QMessageBox.information(self, "Судоку",
                                          "Данные имеют неправильный формат")
    def onOpenFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "Выберите файл", QtCore.QDir.homePath(),
                                                         "Судоку (*.svd)")[0]
        if fileName:
            data = ""
            try:
                with open(fileName, newline="") as f:
                    data = f.read()
            except:
                QtWidgets.QMessageBox.information(self, "Судоку",
                                                  "Не удалось открыть файл")
                return
            if len(data) == 81 or len(data) == 162:
                r = re.compile(r"[^0-9]")
                if not r.match(data):
                    self.widget.setDataAllCells(data)
                    return
            self.dataErrorMsg()

    def onSave(self):
        self.saveSVDFile(self.widget.getDataAllCells())

    def onSaveMini(self):
        self.saveSVDFile(self.widget.getDataAllCellsMini())

    def saveSVDFile(self, data):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         "Выберите файл", QtCore.QDir.homePath(),
                                                         "Судоку (*.svd)")[0]
        if fileName:
            try:
                with open(fileName, mode="w", newline="") as f:
                    f.write(data)
                self.statusBar().showMessage("Файл сохранен", 10000)
            except:
                QtWidgets.QMessageBox.information(self, "Судоку",
                                                  "Не удалось сохранить файл")

