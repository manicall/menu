from modules.ForSave.ModelForSave import ModelForSave
from modules.ForSave.TasksList import TasksList

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
хранит информацию хранящуюся в таблице и в списке задач.
необходимо тк невозможно сохранять таблицу, 
которую видит пользователь
'''
class ForSave:
    def __init__(self):
        # инициализация модели
        self.tl = TasksList()
        self.spanned_cells = [SpannedCells()]
        self.model = ModelForSave()
        self.spanned_cells.pop()

for_save = ForSave()