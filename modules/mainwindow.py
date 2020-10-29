from PyQt5 import QtCore, QtGui, QtWidgets
from modules.widget import Widget, colors
from modules.mydate import myDate
from modules.TasksList.DockWidget import myDockWidget
import webbrowser
import pickle
import subprocess
import sys
from threading import Thread

class MainWindow(QtWidgets.QMainWindow):
    """
    Заполнение меню и строки инструментов элементами;
    привязка действий изображений и горячих клавиш к элементам
    Связывание меню и строки инструментов со строкой состояния.
    Создание постоянного сообщения на строке состояния.
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        self.setWindowTitle("расписание задач")
        self.setWindowIcon(QtGui.QIcon('images\svd.png'))


        self.settings = QtCore.QSettings("config.ini", QtCore.QSettings.IniFormat)
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
        action = self.myMenuModel.addAction("По умолчанию", self.widget.table.this_week)
        action.setStatusTip("текущая неделя")
        self.myMenuModel.addSeparator()
        action = self.myMenuModel.addAction("Неделя", self.widget.table.show_week_table)
        action.setStatusTip("Выбрать неделю")
        action = self.myMenuModel.addAction("Месяц", self.widget.table.show_month_table)
        action.setStatusTip("Выбрать месяц")
        action = self.myMenuModel.addAction("На семестр", self.widget.table.show_semestr_table)
        action.setStatusTip("Показать таблицу по всему семестру")

        # третье меню===============================================
        self.dwAction = menuBar.addAction("Показать список задач", self.dockWidget_visible_control)
        self.dwAction.setStatusTip("Показать список задач")

        # четвертое меню============================================
        action = menuBar.addAction(
            "Открыть расписание",
            lambda : webbrowser.open(r'https://knastu.ru/students/schedule?g=8f699737-a4ce-4303-a349-62b3bb90fe06'))
        action.setStatusTip("Показать список задач")

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
        #======================================================
        self.dw = myDockWidget()
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dw)
        self.dw.visibilityChanged.connect(self.dockWidget_visibility_changed)
        self.dw.tree.model.dataChanged.connect(self.tree_data_changed)

    def tree_data_changed(self):
        self.widget.table.changed = True

    def dockWidget_visibility_changed(self):
        self.status_bar.clearMessage()
        if self.dw.isVisible():
            self.dwAction.setText('Скрыть список задач')
            self.dwAction.setStatusTip('Скрыть список задач')
        else:
            self.dwAction.setText('Показать список задач')
            self.dwAction.setStatusTip('Показать список задач')

    def dockWidget_visible_control(self):
        self.status_bar.clearMessage()
        if self.dw.isVisible():
            self.dwAction.setText('Скрыть список задач')
            self.dwAction.setStatusTip('Скрыть список задач')
            self.dw.setVisible(False)
        else:
            self.dwAction.setText('Показать список задач')
            self.dwAction.setStatusTip('Показать список задач')
            self.dw.setVisible(True)

    # переопределение события закрытия окна
    def closeEvent(self, event):
        if (self.widget.table.changed):
            dialog_result = QtWidgets.QMessageBox.question(
                self,
                "save",
                "Сохранить?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.No)
            if dialog_result == QtWidgets.QMessageBox.Yes:
                self.save()
                event.accept()
            elif dialog_result == QtWidgets.QMessageBox.No:
                event.accept()
            else:
                event.ignore()

    # сохранение информации о таблице в двоичный файл
    def save(self):
        if not self.settings.contains('fileName'):
            self.fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                  "Выберите файл", self.fileName,
                                                                  "Файл (*.svdfl)")[0]
        if self.fileName:
            self.settings.setValue('fileName', self.fileName)
            self.save_tasklist()
            print(self.fileName)
            file = open(self.fileName, "wb")
            pickle.dump(self.widget.table.for_save, file)
            file.close()
            self.widget.table.changed = False


    # открытие информации о таблице
    def read(self, fileName=None):
        if fileName is None:
            self.fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                  "Выберите файл", self.fileName,
                                                                  "Файл (*.svdfl)")[0]
        else:
            self.fileName = fileName
        if self.fileName:
            file = open(self.fileName, "rb")
            from_save = pickle.load(file)
            file.close()
            if from_save.model[0][1].text == self.widget.table.model.item(0,1).text():
                self.settings.setValue('fileName', self.fileName)
                th1 = Thread(target=lambda f=from_save:self.widget.table.input_opened_model(from_save))
                th1.start()
                self.dw.tree.input_opened_model(from_save)
            else: QtWidgets.QMessageBox.critical(self, 'ошибка', "Диапазоны дат не совпадают!")

    # открыть раннее сохраненный файл
    def open_early_file(self):
        if self.settings.contains('fileName'):
            try:
                self.show()
                file = open(self.fileName, "rb")
                from_save = pickle.load(file)
                file.close()
                th1 = Thread(target=lambda f=from_save:self.widget.table.input_opened_model(from_save), daemon=True)
                th1.start()
                self.dw.tree.input_opened_model(from_save)
            except:
                print(sys.exc_info())
            self.widget.table.changed = False


    # обязательный выбор файла при сохранении
    def save_as(self):
        self.fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              "Выберите файл", self.fileName,
                                                              "Файл (*.svdfl)")[0]
        if self.fileName:
            self.settings.setValue('fileName', self.fileName)
            self.save_tasklist()
            print(self.fileName)
            file = open(self.fileName, "wb")
            pickle.dump(self.widget.table.for_save, file)
            file.close()
            self.widget.table.changed = False

    # выбор цвета из меню на toolbar
    def choose_color(self, i):
        try:
            if self.comboBox.currentText() == "Установить цвет ячейки":
                self.widget.set_cell_color(i)
            if self.comboBox.currentText() == "Установить цвет шрифта":
                self.widget.set_font_color(i)
        except:
            pass

    # заново открыть текущую программу
    def clear_all_cells(self):
        # удаление сохраненного имени файла,
        # чтобы пользователь случайно не стер сохраненный ранее файл
        self.settings.clear()
        self.settings.sync()
        self.close()
        # запуск текущей программы
        subprocess.call(['py']+sys.argv)

    def save_tasklist(self):
        tree = self.dw.tree
        for i in range(tree.model.rowCount() - 1):
            parent = tree.model.item(i, 0)
            tree.tl[i].name = parent.text()
            for j in range(parent.rowCount() - 1):
                child = parent.child(j, 0)
                tree.tl[i].subtasks[j].name = child.text()
                tree.tl[i].subtasks[j].checked = child.data(QtCore.Qt.CheckStateRole)
