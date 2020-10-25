from PyQt5 import QtWidgets, QtGui, QtCore
from modules.ForSave.ForSave import for_save
from modules.ForSave.TasksList import myTask, mySubtask
import sys


class TreeView(QtWidgets.QTreeView):
    def __init__(self):
        QtWidgets.QTreeView.__init__(self)
        self.tl = for_save.tl
        self.buttons = []
        self.parents = []
        self.model = QtGui.QStandardItemModel()
        self.set_parent_button()
        self.setHeaderHidden(True)
        self.setModel(self.model)
        self.setAnimated(True)

    def contextMenuEvent(self, event):
        act = (QtWidgets.QAction('удалить', self))
        act.triggered.connect(self.delete)
        QtWidgets.QMenu.exec([act], event.globalPos(), act, self)

    def add_task(self, str='...'):
        self.tl.add_task(myTask(str))
        parent = QtGui.QStandardItem(str)
        parent.setDragEnabled(True)
        parent.setDragEnabled(False)
        self.parents.insert(0, parent)
        self.parents[0].appendRow(QtGui.QStandardItem())
        button = QtWidgets.QPushButton('+')
        button.setFixedWidth(20)
        button.setFixedHeight(20)
        button.setToolTip('Создать подзадачу')
        self.buttons.insert(0, button)
        self.buttons[0].clicked.connect(lambda: self.add_subtask())
        self.model.insertRow(0, self.parents[0])
        self.setIndexWidget(self.parents[0].index().child(0, 0), self.buttons[0])

    def add_subtask(self, i=None, str='...', checkState=0):
        if i is None:
            i = self.currentIndex().parent().row()
        self.tl[i].add_subtask(mySubtask(str, checkState))
        child = QtGui.QStandardItem(str)
        child.setCheckable(True)
        child.setCheckState(checkState)
        print(i, self.parents[i].text())
        self.parents[i].insertRow(0, child)

    def delete(self):  # удалить задачу
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
                    print(ind.parent().row(), ind.row())
                    self.model.item(ind.parent().row(), 0).removeRow(ind.row())
                    self.tl[ind.parent().row()].pop_subtask(ind.row())
            except: print(sys.exc_info())

    def input_opened_model(self, from_save):
        
        self.model.clear()
        self.set_parent_button()
        tl = from_save.tl
        tl.outprint()
        for i in range(len(tl) - 1, -1, -1):
            self.add_task(tl[i].name)
        for i in range(len(tl) - 1, -1, -1):
            for j in range(len(tl[i].subtasks) - 1, -1, -1):
                self.add_subtask(i, tl[i].subtasks[j].name, tl[i].subtasks[j].checked)

    def set_parent_button(self):
        # ============================================
        parent_button = QtWidgets.QPushButton('+')
        parent_button.setFixedWidth(20)
        parent_button.setFixedHeight(20)
        parent_button.clicked.connect(lambda: self.add_task())
        parent_for_button = QtGui.QStandardItem()
        parent_for_button.setSelectable(False)
        parent_for_button.setToolTip('Создать задачу')
        # ============================================
        self.model.appendRow(parent_for_button)
        self.setIndexWidget(self.model.index(0, 0), parent_button)
        # ===========================================
