from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QWidget, QLineEdit, QLabel, QTableWidget, QTableWidgetItem

from datetime import date, datetime
from Classes.dataklassen import Ausgabe
from inspect import signature


class Table(QTableWidget):
    def __init__(self, cl, parent=None):
        self.cl = cl
        a = cl(
            **{k: i.annotation(0) for k, i in signature(cl.__init__).parameters.items()
               if str(i.default) == "<class 'inspect._empty'>" and i.name != "self"}
        )
        super().__init__(0, a.__dict__.keys().__len__(), parent)
        for i, keyname in enumerate(a.__dict__.keys()):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(keyname))
        self.cellDoubleClicked.connect(lambda row, colum: self.removeRow(row))
        self.itemChanged.connect(lambda item: print(item.text()))

    def addrow(self, item):
        r = self.rowCount()
        self.insertRow(r)
        for c, v in enumerate(item.__dict__.values()):
            self.setItem(r, c, QTableWidgetItem(v.__str__()))
