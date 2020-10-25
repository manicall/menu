class mySubtask:
    def __init__(self, name = '...', checked = 0):
        self.name = name
        self.checked = checked


class myTask:
    def __init__(self, name = '...'):
        self.name = name
        self.subtasks = []

    def add_subtask(self, subtask):
        self.subtasks.insert(0, subtask)

    def pop_subtask(self, i):
        print(self.subtasks)
        self.subtasks.pop(i)



class TasksList(list):
    '''
    ikey - индекс задачи
    ivalue - индекс подзадачи
    '''
    def __init__(self):
        list.__init__(self)
    def change_subtask_checked(self, i, j, value):
        self[i].subtasks[j].checked = value

    def add_task(self, task):
        self.insert(0, task)

    def pop_task(self, i):
        self.pop(i)

    def outprint(self):
        for task in self:
            print('task_name:', task.name)
            for subtask in task.subtasks:
                print('   subtask_name:', subtask.name, '| subtask_checked:', subtask.checked)

