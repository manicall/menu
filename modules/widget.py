from PyQt5 import QtCore, QtWidgets, QtGui
from modules.table import Table
from modules.ForSave.ForSave import myItem, SpannedCells
from modules.myDialog import MyDialog
import sys

colors = [
    '#FFFFFF',
    '#808080',
    '#C0C0C0',
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
    '#7B68EE',
    '#000080',
    '#000000'
]

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
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
        # функции
        funcs = []
        funcs.append(self.span_cells)
        funcs.append(self.add_icon)
        funcs.append(self.delete_icon)
        # соединить функцию и действия
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
        # запоминает изменения
        self.table.for_save.model.set_item(row, column, myItem(icon=dialog.choosen_path))

    def delete_icon(self):
        row, column = (self.table.view.currentIndex().row(), self.table.view.currentIndex().column())
        self.table.model.setData(self.table.model.index(row, column), None, role=QtCore.Qt.DecorationRole)
        # запоминает изменения
        self.table.for_save.model.set_item(row, column, myItem(icon=None))

    # объединение ячеек
    def span_cells(self):
        span = self.get_span()
        if span.column > 0:
            self.table.view.setSpan(span.row, span.column, span.rowSpan, span.columnSpan)
            # запоминает изменения
            self.table.for_save.spanned_cells.append(
                SpannedCells(span.row, span.column, span.rowSpan, span.columnSpan))

    def set_cell_color(self, index):
        current_color_index = index
        span = self.get_span()
        for i in range(span.row, span.row + span.rowSpan):
            for j in range(span.column, span.column + span.columnSpan):
                self.table.model.item(i, j).setBackground(
                    QtGui.QBrush(QtGui.QColor(colors[current_color_index])))  # устанавливает цвет фона
                # запоминает изменения
                if self.table.for_save.model[i][j] is not None:
                    self.table.for_save.model[i][j].background_color = colors[current_color_index]
                else:
                    self.table.for_save.model.set_item(i, j, myItem(background_color=colors[current_color_index]))

    def set_font_color(self, index):
        current_color_index = index
        span = self.get_span()
        for i in range(span.row, span.row + span.rowSpan):
            for j in range(span.column, span.column + span.columnSpan):
                self.table.model.item(i, j).setForeground(
                    QtGui.QBrush(QtGui.QColor(colors[current_color_index]))) # устанавливает цвет шрифта
                # запоминает изменения
                if self.table.for_save.model[i][j] is not None:
                    self.table.for_save.model[i][j].font_color = colors[current_color_index]
                else:
                    self.table.for_save.model.set_item(i, j, myItem(font_color=colors[current_color_index]))

    # получить интервал выбранных ячеек
    def get_span(self):
        first_row = self.table.view.selectedIndexes()[0].row()
        first_column = self.table.view.selectedIndexes()[0].column()
        last_row = self.table.view.selectedIndexes()[-1].row()
        last_column = self.table.view.selectedIndexes()[-1].column()
        rowSpan = last_row - first_row + 1              # количество выбранных строк
        columnSpan = last_column - first_column + 1     # количество выбранных столбцов
        return SpannedCells(first_row, first_column, rowSpan, columnSpan)
