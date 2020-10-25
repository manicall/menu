from PyQt5 import QtWidgets, QtGui, QtCore
from modules.ForSave.ForSave import for_save
class TreeView(QtWidgets.QTreeView):
    def __init__(self):
        QtWidgets.QTreeView.__init__(self)
        self.tl = for_save.tl
        self.buttons = []
        self.parents = []
        self.count = 0
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
        act = (QtWidgets.QAction('удалить', self))
        act.triggered.connect(self.delete)
        QtWidgets.QMenu.exec([act], event.globalPos(), act, self)

    def add_task(self, str='...'):
        self.tl.add_task('...')
        parent = QtGui.QStandardItem(str)
        parent.setDragEnabled(True)
        parent.setDragEnabled(False)
        self.parents.append(parent)
        self.parents[-1].appendRow(QtGui.QStandardItem())
        button = QtWidgets.QPushButton('+')
        button.setFixedWidth(20)
        button.setFixedHeight(20)
        button.setToolTip('Создать подзадачу')
        self.buttons.append(button)
        self.buttons[-1].clicked.connect(lambda event, i=self.count: self.add_subtask(event, i))
        self.model.insertRow(0, self.parents[-1])
        self.setIndexWidget(self.parents[-1].index().child(0, 0), self.buttons[-1])
        self.count += 1

    def add_subtask(self, event, i, str='...'):
        self.tl.add_subtask(i, str)
        child = QtGui.QStandardItem(str)
        child.setCheckable(True)
        self.parents[i].insertRow(0, child)

    def delete(self):
        ind = self.currentIndex()
        if ind.isValid():
            ind_child = ind.child(0, 0)
            if ind_child.isValid():
                pass
                # выбран родитель
                self.model.removeRow(ind.row())
                self.tl.pop_task()
            else:
                # выбран ребенок
                self.model.item(ind.parent().row(), 0).removeRow(0)
                self.tl.pop_subtask()

    def input_opened_model(self, from_save):
        print(from_save.tl)
        i = 0
        j = 0
        """
        for task in from_save.tl[::-1]:
            self.add_task(list(task.keys())[0])
            for subtasks in list(task.values()):
                i += 1
                print('i:',i)
                print(len(subtasks), type(subtasks))
                if not isinstance(subtasks, list): list(subtasks)
                for i in range(len(subtasks)):
                    j += 1
                    print('j:', j)
                    self.add_subtask(False, i, subtasks[i])
        """


