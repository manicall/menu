class TasksList(list):
    '''
    ikey - индекс задачи
    ivalue - индекс подзадачи
    '''
    def __init__(self):
        list.__init__(self)

    def add_task(self, key='...'):
        self.insert(0, {key : []})

    def add_subtask(self, ikey, value):
        ikey = len(self) - int(ikey) - 1
        self[ikey][self.get_task_name(ikey)].insert(0, value)

    def change_task_name(self, ikey, key):
        # присваивает список значений ключа
        values = self[ikey][self.get_task_name(ikey)]
        # удаляет элемент по ключу
        self[ikey].pop(self.get_task_name(ikey))
        # добавляет словарь
        self[ikey][key] = values

    def change_subtask_name(self, ikey, ivalue, value):
        print(ikey, ivalue)
        self[ikey][self.get_task_name(ikey)][ivalue] = value

    def change_subtasks_name(self, ikey, value):
        if isinstance(value, list):
            self[ikey][self.get_task_name(ikey)] = value
        else:
            print("в качестве аргумента value ожидается список")

    def pop_task(self, ikey):
        self.pop(ikey)

    def pop_subtask(self, ikey, ivalue):
        self[ikey][self.get_task_name(ikey)].pop(ivalue)

    def get_task_name(self, ikey):
        return list(self[ikey].keys())[0]
