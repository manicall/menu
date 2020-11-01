from PyQt5 import QtWidgets, QtGui, QtCore
from modules.TasksList.TreeView import TreeView

class myDockWidget(QtWidgets.QDockWidget):
    def __init__(self):
        QtWidgets.QDockWidget.__init__(self, 'Список задач')
        self.tree = TreeView()
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                            QtWidgets.QDockWidget.DockWidgetMovable |
                            QtWidgets.QDockWidget.DockWidgetClosable)
        self.setFloating(True)
        self.setVisible(False)
        self.setWidget(self.tree)

