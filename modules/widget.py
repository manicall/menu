from PyQt5 import QtCore, QtWidgets, QtGui
from modules.table import Table
from modules.models import myItem, SpannedCells
from modules.myDialog import MyDialog

colors = [
'#000000',
'#808080',
'#C0C0C0',
'#FFFFFF',
'#FF00FF',
'#800080',
'#FF0000',
'#800000',
'#FFFF00',
'#808000',
'#00FF00',
'#008000',
'#00FFFF',
'#008080',
'#0000FF',
'#000080'
]


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.current_color_index = None
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.table = Table()
        vBoxMain = QtWidgets.QVBoxLayout()
        vBoxMain.addWidget(self.table.view)
        self.setLayout(vBoxMain)

    def contextMenuEvent(self, event):
        # действия
        acts = []
        acts.append(QtWidgets.QAction('Объединить/разделить', self))
        acts.append(QtWidgets.QAction("Вставить иконку", self))
        acts.append(QtWidgets.QAction("Удалить иконку", self))
        acts.append(QtWidgets.QAction("Установить цвет ячейки", self))
        acts.append(QtWidgets.QAction("Установить цвет шрифта", self))
        # функции
        funcs = []
        funcs.append(self.span_cells)
        funcs.append(self.add_icon)
        funcs.append(self.delete_icon)
        funcs.append(self.set_cell_color)
        funcs.append(self.set_font_color)
        # соединить функцию и действия =
        for i in range(len(acts)):
            acts[i].triggered.connect(funcs[i])
        # вызвать меню
        QtWidgets.QMenu.exec(acts, event.globalPos(), acts[0], self)

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

    def set_cell_color(self):
        if self.current_color_index is not None:
            row, column = self.table.view.currentIndex().row(), self.table.view.currentIndex().column()
            self.table.model.item(row, column).setBackground(QtGui.QBrush(QtGui.QColor(colors[self.current_color_index])))
            if self.table.model_for_save.model[row][column] is not None:
                self.table.model_for_save.model[row][column].background_color = colors[self.current_color_index]
            else:
                self.table.model_for_save.set_item(background_color=colors[self.current_color_index])

    def set_font_color(self):
        if self.current_color_index is not None:
            row, column = self.table.view.currentIndex().row(), self.table.view.currentIndex().column()
            self.table.model.item(row, column).setForeground(
                QtGui.QBrush(QtGui.QColor(colors[self.current_color_index])))
            if self.table.model_for_save.model[row][column] is not None:
                self.table.model_for_save.model[row][column].font_color = colors[self.current_color_index]
            else:
                self.table.model_for_save.set_item(font_color=colors[self.current_color_index])
