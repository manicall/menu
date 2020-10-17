from PyQt5 import QtCore, QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
settings = QtCore.QSettings("max", "menu")
v1 = 12
print("Сохраняем настройки")
settings.setValue("Значение 1", v1)
#settings.sync()
print("Считываем настройки")
lv1 = settings.value("Значение 1")
print(lv1)