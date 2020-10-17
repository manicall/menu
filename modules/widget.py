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
        self.table.show_default_table()

    def span_cells(self):
        row, column = (self.table.view.currentIndex().row(), self.table.view.currentIndex().column())
        if row > 0:
            rowSpan, columnSpan = self.table.view.selectedIndexes()[0].row(),\
                                   self.table.view.selectedIndexes()[0].column()
            self.table.view.setSpan(rowSpan, columnSpan, row - rowSpan + 1, column - columnSpan + 1)
            print(row, column, rowSpan, columnSpan)
        else:
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', 'Чтобы объединить ячейки их необходимо выбрать')
