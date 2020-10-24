'''
хранит информацию хранящуюся в ячейке
'''
class myItem:
    def __init__(self, text='', icon=None, font_color='#000000', background_color='#ffffff'):
        self.text = text
        self.icon = icon
        self.font_color = font_color
        self.background_color = background_color


'''
хранит информацию об объединенных ячейках
'''
class SpannedCells:
    def __init__(self, row=-1, column=-1, rowSpan=0, columnSpan=0):
        self.row = row
        self.column = column
        self.rowSpan = rowSpan
        self.columnSpan = columnSpan


'''
хранит информацию хранящуюся в таблице.
необходимо тк невозможно сохранять таблицу, 
которую видит пользователь
'''


class ForSave:
    def __init__(self, rows, cols):
        # инициализация модели
        self.rowCount = rows
        self.columnCount = cols
        self.spanned_cells = [SpannedCells()]
        self.model = [[myItem()]]

        # очистка контейнеров
        self.model.pop()
        self.spanned_cells.pop()
        # заполнение модели пустыми значениями
        for i in range(rows):
            self.model.append([])
        for i in range(rows):
            for j in range(cols):
                self.model[i].append(None)

    def set_item(self, row, column, myItem):
        if self.model[row][column] == None:
            self.model[row].pop(column)
            self.model[row].insert(column, myItem)
        else:
            if myItem.text != '':
                self.model[row][column].text = myItem.text
            if myItem.icon != None:
                self.model[row][column].icon = myItem.icon
            if myItem.font_color != '#000000':
                self.model[row][column].font_color = myItem.font_color
            if myItem.background_color != '#ffffff':
                self.model[row][column].background_color = myItem.background_color
