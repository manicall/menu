import pickle
from PyQt5 import QtWidgets, QtGui
from modules.mainwindow import MainWindow
import sys

app = QtWidgets.QApplication(sys.argv)
desktop = QtWidgets.QApplication.desktop().availableGeometry()
window = MainWindow()
window.setWindowTitle("Класс QTableView")
window.move(0, 0)
window.resize(desktop.width() // 2 + 110, QtWidgets.QApplication.desktop().height() // 2)
f = open(r"C:\Users\max\desktop\file.txt", "wb")
obj = QtGui.QImage(r"images/new.png")
print(obj)
pickle.dump(obj, f)
sys.exit(app.exec_())
