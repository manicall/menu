# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore
from modules.mainwindow import MainWindow

app = QtWidgets.QApplication(sys.argv)
desktop = QtWidgets.QApplication.desktop().availableGeometry()
window = MainWindow()
window.move(0, 0)
window.resize(int(desktop.width() * (3/4)), int(QtWidgets.QApplication.desktop().height() * (9/16)))
window.open_early_file()
window.show()
window_result = app.exec()
dialog_result = QtWidgets.QMessageBox.question(window,
                                        "save",
                                        "Сохранить?",
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                        QtWidgets.QMessageBox.No)
if dialog_result == QtWidgets.QMessageBox.Yes:
    window.save()
sys.exit(window_result)
