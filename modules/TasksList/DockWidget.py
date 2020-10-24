from PyQt5 import QtWidgets, QtGui, QtCore


class TreeView:
    def __init__(self):
        self.buttons = []
        self.parents = []
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
        self.view = QtWidgets.QTreeView()
        self.view.setHeaderHidden(True)
        self.view.setModel(self.model)
        self.view.setAnimated(True)
        self.view.setIndexWidget(self.model.index(0, 0), parent_button)
        self.count = 0

    def add_task(self):

        self.parents.append(QtGui.QStandardItem('...'))
        self.parents[-1].appendRow(QtGui.QStandardItem())
        button = QtWidgets.QPushButton('+')
        button.setFixedWidth(20)
        button.setFixedHeight(20)
        button.setToolTip('Создать подзадачу')
        self.buttons.append(button)
        self.buttons[-1].clicked.connect(lambda event, i=self.count: self.add_subtask(event, i))
        self.model.insertRow(0, self.parents[-1])
        self.view.setIndexWidget(self.parents[-1].index().child(0, 0), self.buttons[-1])
        self.count += 1

    def add_subtask(self, event, i):
        print(i)
        child = QtGui.QStandardItem('...')
        child.setCheckable(True)
        self.parents[i].insertRow(0, child)

class myDockWidget():
    def __init__(self):
        self.tree = TreeView()
        self.dw = QtWidgets.QDockWidget('Список задач')
        self.dw.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.dw.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                            QtWidgets.QDockWidget.DockWidgetMovable |
                            QtWidgets.QDockWidget.DockWidgetClosable)
        self.dw.setFloating(True)
        self.dw.setVisible(False)
        self.dw.setWidget(self.tree.view)
