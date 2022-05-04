#!/usr/bin/python3

# This Python file uses the following encoding: utf-8
# main_widget.py BSZET-DD Template
# Copyright © 2022 by SRE
import sys
import os
import json
from PySide6.QtUiTools import loadUiType
from PySide6 import QtCore as Core
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from datetime import date, datetime
from Classes.dataklassen import Ausgabe


QT_API = "PySide6"



UIFilename = "form.ui"
ProjectDir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(ProjectDir, UIFilename))

def umlaute_zu_buchstaben(umlaut):
    umlaut = ["ä", "ü", "ö", "ß"]



class MainFrm(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        ausgabe:
    @Core.Slot()
    def on_ausgabeBtn_clicked(self):

        ausgaben_datum = self.ausgaben_date.date().toPyDateTime()
        ausgaben_kategorie = self.ausgaben_kat.currentText()
        ausgaben_mwst = self.ausgaben_mwst.currentText()
        self.test_lbl.setText(ausgaben_datum)

    @Core.Slot()
    def on_openBtn_clicked(self):
        filename = QFileDialog.getOpenFileName()[0]
        with open(filename,"r+") as f:
            objectsDict = json.loads(f.read())

            self.test_lbl.setText(Ausgabe.fromDict(objectsDict).__str__())


    @Core.Slot()
    def on_saveBtn_clicked(self):
        filename = QFileDialog.getSaveFileName()[0]
        with open(filename,"w+") as f:
            f.write(json.dumps(Ausgabe("Du bist dumm", date.today()).toDict()))


if __name__ == "__main__":
    Core.QCoreApplication.setAttribute(Core.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrm()
    widget.show()

    sys.exit(app.exec())
