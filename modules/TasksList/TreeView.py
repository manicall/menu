from PyQt5 import QtWidgets, QtGui, QtCore
from modules.ForSave.ForSave import for_save
from modules.ForSave.TasksList import myTask, mySubtask
from modules.ForSave import ForSave
import sys
import traceback

class TreeView(QtWidgets.QTreeView):
    def __init__(self):
        QtWidgets.QTreeView.__init__(self)
        self.tl = for_save.tl
        self.buttons = []
        self.parents = []
        self.settings = QtCore.QSettings("experement.ini", QtCore.QSettings.IniFormat)
        # ============================================
        parent_button = QtWidgets.QPushButton('+')
        parent_button.setFixedWidth(20)
        parent_button.setFixedHeight(20)
        parent_button.clicked.connect(lambda: self.add_task())
        parent_for_button = QtGui.QStandardItem()
        parent_for_button.setSelectable(False)
        parent_for_button.setToolTip('Создать задачу')
        # ============================================
        self.model = QtGui.QStandardItemModel()
        self.model.appendRow(parent_for_button)
        # ===========================================
        self.setHeaderHidden(True)
        self.setModel(self.model)
        self.setAnimated(True)
        self.setIndexWidget(self.model.index(0, 0), parent_button)

    def contextMenuEvent(self, event):
        act1 = (QtWidgets.QAction('удалить', self))
        act1.triggered.connect(self.delete)
        act2 = (QtWidgets.QAction('переименовать', self))
        act2.triggered.connect(lambda: self.edit(self.currentIndex().sibling(self.currentIndex().row(), 0)))
        QtWidgets.QMenu.exec([act1, act2], event.globalPos(), act1, self)

    def add_task(self, str='...'):
        # глобальная переменная, регистрирующая изменения в файле
        ForSave.changed = True
        # добавляем задачу в список для сохранения
        self.tl.add_task(myTask(str))
        # создание текстового поля задачи
        parent = QtGui.QStandardItem(str)
        # вставка текстового поля в контейнер
        self.parents.insert(0, parent)
        # добавление поля для кнопки, которая будет создавать подзадачи
        item_for_button = QtGui.QStandardItem('')
        item_for_button.setSelectable(False)
        self.parents[0].appendRow(item_for_button)
        # описание кнопки для создания подзадачи
        button = QtWidgets.QPushButton('+')
        button.setFixedWidth(20)
        button.setFixedHeight(20)
        button.setToolTip('Создать подзадачу')
        # вставка кнопки в контейнер кнопок
        self.buttons.insert(0, button)
        # добавление подзадачи на нажатие на кнопку
        self.buttons[0].clicked.connect(lambda: self.add_subtask())
        # вставка текстового поля в модель
        self.model.insertRow(0, self.parents[0])
        # вставка кнопки на поле для кнопки
        self.setIndexWidget(self.parents[0].index().child(0, 0), self.buttons[0])
        self.edit(self.currentIndex().sibling(0, 0))

    def add_subtask(self, i=None, str='...', checkState=0):
        ForSave.changed = True
        if i is None:
            # индекс задачи, для выбранной под задачи
            i = self.currentIndex().parent().row()
        # добавление подзадачи в список для сохранения
        self.tl[i].add_subtask(mySubtask(str, checkState))
        # описание подзадачи
        child = QtGui.QStandardItem(str)
        child.setCheckable(True)
        child.setCheckState(checkState)
        # вставка подзадачи в задачу
        self.parents[i].insertRow(0, child)
        # режим редактирования для добавленной задачи
        self.edit(self.currentIndex().sibling(0, 0))

    def delete(self):  # удалить задачу
        ForSave.changed = True
        ind = self.currentIndex()
        if ind.isValid():
            try:
                ind_child = ind.child(0, 0)
                if ind_child.isValid():
                    # выбран родитель
                    self.parents.pop(ind.row())
                    self.model.removeRow(ind.row())
                    self.tl.pop_task(ind.row())
                else:
                    # выбран ребенок
                    if ind.row() != self.model.item(ind.parent().row(), 0).rowCount() - 1:
                        self.model.item(ind.parent().row(), 0).removeRow(ind.row())
                        self.tl[ind.parent().row()].pop_subtask(ind.row())
            except:
                traceback.print_tb(sys.exc_info()[2], file=sys.stdout)
                print('ERROR:', sys.exc_info()[1])

    def input_opened_model(self, from_save):
        tl = from_save.tl
        for i in range(len(tl) - 1, -1, -1):
            self.add_task(tl[i].name)
        for i in range(len(tl) - 1, -1, -1):
            for j in range(len(tl[i].subtasks) - 1, -1, -1):
                self.add_subtask(i, tl[i].subtasks[j].name, tl[i].subtasks[j].checked)
