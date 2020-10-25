# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore
from modules.mainwindow import MainWindow
import time
start_time = time.time()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    desktop = QtWidgets.QApplication.desktop().availableGeometry()
    window = MainWindow()
    window.move(0, 0)
    window.resize(int(desktop.width()) - 100, int(QtWidgets.QApplication.desktop().height() * (9/16)))
    window.open_early_file()
    window.show()
    print("--- %s seconds ---" % (time.time() - start_time))
    window_result = app.exec()
    sys.exit(window_result)
