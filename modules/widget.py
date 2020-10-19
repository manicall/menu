from PyQt5 import QtCore, QtWidgets, QtGui
from modules.table import Table, Models
from modules.models import SpannedCells
from modules.myDialog import MyDialog
import sys

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.table = Table()
        vBoxMain = QtWidgets.QVBoxLayout()
        vBoxMain.addWidget(self.table.view)
        self.setLayout(vBoxMain)

    def contextMenuEvent(self, event):
        act1 = QtWidgets.QAction("Вставить иконку", self)
        act1.triggered.connect(self.add_icon)
        act2 = QtWidgets.QAction("удалить иконку", self)
        act2.triggered.connect(self.delete_icon)
        QtWidgets.QMenu.exec([act1, act2], event.globalPos(),
                             act2, self)

    def add_icon(self):
        dialog = MyDialog()
        dialog.exec_()
        row, column = (self.table.view.currentIndex().row(), self.table.view.currentIndex().column())
        self.table.model.setData(self.table.model.index(row, column), QtGui.QIcon(dialog.choosen_path),
                           role=QtCore.Qt.DecorationRole)

    def delete_icon(self):
        try:
            row, column = (self.table.view.currentIndex().row(), self.table.view.currentIndex().column())
            self.table.model.setData(self.table.model.index(row, column), None, role=QtCore.Qt.DecorationRole)
        except: print(sys.exc_info())

    # очистка ячеек
    def clear_all_cells(self):
        self.table.model.clear()
        self.table.model = Models().model
        self.table.view.setModel(self.table.model)
        self.table.view.resizeRowToContents(0)
        self.table.show_default_table()
        self.table.view.clearSpans()

    # объединение ячеек
    def span_cells(self):
        row, column = (self.table.view.currentIndex().row(), self.table.view.currentIndex().column())
        if row > 0:
            rowSpan, columnSpan = self.table.view.selectedIndexes()[0].row(), \
                                  self.table.view.selectedIndexes()[0].column()
            self.table.view.setSpan(rowSpan, columnSpan, row - rowSpan + 1, column - columnSpan + 1)
            print(rowSpan, columnSpan,
                  row - rowSpan + 1,
                  column - columnSpan + 1)
            self.table.model_for_save.spanned_cells.append(SpannedCells(rowSpan, columnSpan,
                                                                        row - rowSpan + 1,
                                                                        column - columnSpan + 1))
        else:
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', 'Чтобы объединить ячейки их необходимо выбрать')
