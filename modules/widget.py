from PyQt5 import QtCore, QtWidgets, QtGui
from modules.table import Table, Models
from modules.models import myItem, SpannedCells
from modules.myDialog import MyDialog


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.table = Table()
        vBoxMain = QtWidgets.QVBoxLayout()
        vBoxMain.addWidget(self.table.view)
        self.setLayout(vBoxMain)

    def contextMenuEvent(self, event):
        act1 = QtWidgets.QAction('Объединить/разделить', self)
        act1.triggered.connect(self.span_cells)
        act2 = QtWidgets.QAction("Вставить иконку", self)
        act2.triggered.connect(self.add_icon)
        act3 = QtWidgets.QAction("Удалить иконку", self)
        act3.triggered.connect(self.delete_icon)
        QtWidgets.QMenu.exec([act1, act2, act3], event.globalPos(), act1, self)

    def add_icon(self):
        dialog = MyDialog()
        dialog.move(QtGui.QCursor.pos())
        dialog.exec()
        row, column = (self.table.view.currentIndex().row(), self.table.view.currentIndex().column())
        self.table.model.setData(self.table.model.index(row, column), QtGui.QIcon(dialog.choosen_path),
                                 role=QtCore.Qt.DecorationRole)
        self.table.model_for_save.set_item(row, column, myItem(icon=dialog.choosen_path))

    def delete_icon(self):
        row, column = (self.table.view.currentIndex().row(), self.table.view.currentIndex().column())
        self.table.model.setData(self.table.model.index(row, column), None, role=QtCore.Qt.DecorationRole)
        self.table.model_for_save.set_item(row, column, myItem(icon=None))

    # объединение ячеек
    def span_cells(self):
        first_row, first_column = self.table.view.selectedIndexes()[0].row(), \
                                  self.table.view.selectedIndexes()[0].column()
        if first_column > 0:
            last_row, last_column = self.table.view.selectedIndexes()[-1].row(), \
                                    self.table.view.selectedIndexes()[-1].column()
            rowSpan, columnSpan = last_row - first_row + 1, last_column - first_column + 1
            self.table.view.setSpan(first_row, first_column, rowSpan, columnSpan)
            self.table.model_for_save.spanned_cells.append(
                SpannedCells(first_row, first_column, rowSpan, columnSpan))

