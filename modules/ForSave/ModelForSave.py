class ModelForSave(list):
    def __init__(self):
        self.rowCount = 0
        self.columnCount = 0

        # заполнение модели пустыми значениями
    def set_item(self, row, column, myItem):
        if self[row][column] == None:
            self[row].pop(column)
            self[row].insert(column, myItem)
        else:
            if myItem.text != '':
                self[row][column].text = myItem.text
            if myItem.icon != None:
                self[row][column].icon = myItem.icon
            if myItem.font_color != '#000000':
                self[row][column].font_color = myItem.font_color
            if myItem.background_color != '#ffffff':
                self[row][column].background_color = myItem.background_color

    def set_size(self, rows, cols):
        if rows != 0 and cols != 0:
            self.rowCount = rows
            self.columnCount = cols
            for i in range(rows):
                self.append([])
            for i in range(rows):
                for j in range(cols):
                    self[i].append(None)
        else:
            print("размеры модели уже установлены")

