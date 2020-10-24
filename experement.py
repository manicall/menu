from PyQt5 import QtWidgets, Qt


def clickme():
    index = tree.currentIndex().row()
    item = model.item(index)
    print(item.text())
    item.setIcon(icons[0])


app = Qt.QApplication([])
main_window = QtWidgets.QWidget()

btn = Qt.QPushButton("Click me", main_window)
btn.clicked.connect(clickme)

icons = (Qt.QIcon('tick_green.png'), Qt.QIcon('tick_red.png'))
model = Qt.QStandardItemModel()
model.setHorizontalHeaderLabels([u'Заголовок'])

for i in range(5):
    item = Qt.QStandardItem(f'text {i}')
    item.setIcon(icons[1])
    model.appendRow(item)

tree = QtWidgets.QTreeView(main_window)
tree.setModel(model)

grid = QtWidgets.QGridLayout(main_window)
grid.setContentsMargins(0, 0, 0, 0)
grid.addWidget(tree, 0, 0)
grid.addWidget(btn, 1, 0)

main_window.move(0, 0)
main_window.show()
app.exec_()