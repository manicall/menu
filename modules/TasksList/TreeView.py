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
        self.expanded.connect(self.onExpanded)

    def contextMenuEvent(self, event):
        # действия
        acts = []
        acts.append(QtWidgets.QAction('удалить задачу', self))
        acts.append(QtWidgets.QAction('удалить подзадачу', self))
        # функции
        funcs = []
        funcs.append(self.delete_task)
        funcs.append(self.delete_subtask)
        # соединить функцию и действия
        for i in range(len(acts)):
            acts[i].triggered.connect(funcs[i])
        # вызвать меню
        QtWidgets.QMenu.exec(acts, event.globalPos(), acts[0], self)

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
        print(self.parents[i])