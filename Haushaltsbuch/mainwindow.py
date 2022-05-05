#!/usr/bin/python3

# This Python file uses the following encoding: utf-8
# main_widget.py BSZET-DD Template
# Copyright © 2022 by SRE
import sys
import os

from PySide6.QtUiTools import loadUiType
from PySide6 import QtCore as Core
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter


import json
from datetime import date, datetime

from Classes.dataklassen import Ausgabe, Einahme, Berechnung

QT_API = "PySide6"
UIFilename = "form.ui"
ProjectDir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(ProjectDir, UIFilename))

ausgaben_liste = []
einnamen_liste = []


class MainFrm(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.p = None
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionNew.triggered.connect(self.newProject)
        self.berechnung = None


    @Core.Slot()
    def on_ausgabeBtn_clicked(self):
        ausgaben_artikel = self.ausgaben_artikel.text()
        ausgaben_preis =self.ausgaben_preis.text()
        #ausgaben_datum = self.ausgaben_date.date().toPyDateTime()
        ausgaben_kategorie = self.ausgaben_kat.currentText()
        ausgaben_mwst = self.ausgaben_mwst.currentText()
        einkommen_höhe = self.einkommen_hoehe.text()
        einnamen_liste.append(einkommen_höhe)
        ausgaben_liste.append(ausgaben_preis)
        #self.test_lbl.setText(ausgaben_datum)
        ausgaben_insgesamt = 0.00
        print(ausgaben_insgesamt)
        for i in ausgaben_liste:
            print(i)
            i = i.replace("€", "")
            ausgaben_insgesamt = ausgaben_insgesamt-float(i)
        print(ausgaben_insgesamt)
        self.test_lbl.setText(str(ausgaben_insgesamt))

    def openFile(self):
        filename = QFileDialog.getOpenFileName()[0]
        with open(filename,"r+") as f:
            objectsDict = json.loads(f.read())

            self.test_lbl.setText(Ausgabe.fromDict(objectsDict).__str__())

    def saveFile(self):
        filename = QFileDialog.getSaveFileName()[0]
        with open(filename,"w+") as f:
            f.write(json.dumps(Ausgabe("Du bist dumm", date.today()).toDict()))

    def newProject(self):
        self.p = PopUp(self)

    def setProject(self, b):
        self.berechnung = b


class PopUp(QtWidgets.QWidget):
    def __init__(self, main):
        QWidget.__init__(self)
        self.resize(200, 200)
        self.nametextfield = QTextEdit(self)
        self.nametextfield.setGeometry(QRect(0, 0, 200, 75))
        self.nametextfield.setText("Name des Projektes")
        self.authortextfield = QTextEdit(self)
        self.authortextfield.setGeometry(QRect(0, 75, 200, 75))
        self.authortextfield.setText("Author des Projektes")
        self.createbtn = QPushButton(self, text="create Project")
        self.createbtn.setGeometry(QRect(0, 150, 200, 50))
        self.createbtn.clicked.connect(self.createBerechnung)
        self.authortextfield.show()
        self.nametextfield.show()
        self.createbtn.show()
        self.show()
        self.main = main

    def createBerechnung(self):
        self.main.setProject(
            Berechnung(
                name=self.nametextfield.toPlainText(),
                author=self.authortextfield.toPlainText()
            )
        )
        self.close()


if __name__ == "__main__":
    Core.QCoreApplication.setAttribute(Core.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrm()
    widget.show()

    sys.exit(app.exec())
