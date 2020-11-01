# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore
from modules.mainwindow import MainWindow
import time
import re
start_time = time.time()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    desktop = QtWidgets.QApplication.desktop().availableGeometry()
    window = MainWindow()
    window.move(0, 0)
    window.resize(int(desktop.width()) - 100, int(QtWidgets.QApplication.desktop().height() * (9/16)))

    # открытие файла
    p = re.compile(r".\.svdfl")
    if len(sys.argv) > 1:
        if p.search(sys.argv[1]):
            window.read(sys.argv[1])
        else:
            QtWidgets.QMessageBox().critical(window, "", "Формат данного файла не поддерживается!")
            exit(1)
    else:
        window.open_early_file()
    window.show()
    print("--- %s seconds ---" % (time.time() - start_time))
    window_result = app.exec()
    sys.exit(window_result)
