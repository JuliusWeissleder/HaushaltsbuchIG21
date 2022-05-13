import sys
import os
from widgets.tablewidget import Table
from PySide6.QtUiTools import loadUiType
from PySide6 import QtCore as Core
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel
from Classes.dataklassen import Ausgabe


if __name__ == "__main__":
    Core.QCoreApplication.setAttribute(Core.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    widget = Table(Ausgabe)
    widget.addrow(Ausgabe(5.1, 19, "kat", "Haus"))
    widget.show()

    sys.exit(app.exec())
