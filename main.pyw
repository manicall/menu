# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from modules.mainwindow import MainWindow

app = QtWidgets.QApplication(sys.argv)
desktop = QtWidgets.QApplication.desktop().availableGeometry()
window = MainWindow()
window.move(0, 0)
window.resize(int(desktop.width() * (3/4)), int(QtWidgets.QApplication.desktop().height() * (9/16)))
window.open_early_file()
window.show()
sys.exit(app.exec_())
