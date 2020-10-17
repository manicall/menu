from PyQt5 import QtCore, QtWidgets
from modules.table import Table, Models
class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.table = Table()
        vBoxMain = QtWidgets.QVBoxLayout()
        vBoxMain.addWidget(self.table.view)
        self.setLayout(vBoxMain)

    def clear_all_cells(self):
        self.table.model.clear()
        self.table.model = Models().model
        self.table.view.setModel(self.table.model)
        self.table.view.resizeRowToContents(0)