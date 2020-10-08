# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtWidgets

from modules.mainwindow import MainWindow

app = QtWidgets.QApplication(sys.argv)
desktop = QtWidgets.QApplication.desktop().availableGeometry()
window = MainWindow()
window.setWindowTitle("Класс QTableView")
window.move(0, 0)
window.resize(desktop.width() // 2, QtWidgets.QApplication.desktop().height() // 2)
window.show()
sys.exit(app.exec_())
