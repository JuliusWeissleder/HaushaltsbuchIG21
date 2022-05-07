#!/usr/bin/python3

import sys
import os

from PySide6.QtUiTools import loadUiType
from PySide6 import QtCore as Core
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel
from PySide6.QtCore import QRect
from PySide6.QtGui import QShortcut, QKeySequence

import json
from datetime import date, datetime

from Classes.dataklassen import Ausgabe, Einahme, Berechnung

QT_API = "PySide6"
UIFilename = "form.ui"
ProjectDir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(ProjectDir, UIFilename))


class MainFrm(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.openSC = QShortcut(QKeySequence("Ctrl+o"), self)
        self.openSC.activated.connect(self.openFile)
        self.newSC = QShortcut(QKeySequence("Ctrl+n"), self)
        self.newSC.activated.connect(self.newProject)
        self.saveSC = QShortcut(QKeySequence("Ctrl+s"), self)
        self.saveSC.activated.connect(self.fileSave)
        self.saveAsSC = QShortcut(QKeySequence("Ctrl+Shift+s"), self)
        self.saveAsSC.activated.connect(self.fileSaveAs)

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.fileSave)
        self.actionNew.triggered.connect(self.newProject)

        self.btn_add_ausgaben.clicked.connect(self.newAusgabe)
        self.btn_add_einkommen.clicked.connect(self.newEinkommen)

        self.berechnung = None

    def noProjectExecption(self):
        QMessageBox.information(
            self,
            "No Projekt",
            "U haven't created a Projekt yet.\n Create one with File -> new",
        )

    def newEinkommen(self):
        try:
            self.berechnung.addEinahme(
                Einahme(
                    int(self.einkommen_hoehe.text()),
                    str(self.einkommen_kat.currentText())
                )
            )
        except AttributeError:
            self.noProjectExecption()
        self.werteAus()

    def newAusgabe(self):
        try:
            self.berechnung.addAusgabe(
                Ausgabe(
                    int(self.ausgaben_preis.text()),
                    int(str(self.ausgaben_mwst.currentText()).replace("%", "")),
                    str(self.ausgaben_kat.currentText()),
                    str(self.ausgaben_artikel.text())
                )
            )
        except AttributeError:
            self.noProjectExecption()
        self.werteAus()

    def werteAus(self):
        self.lbl_test.setText(
            str(self.berechnung.getDifferenz())
        )

    def openFile(self):
        filename = QFileDialog.getOpenFileName()[0]
        with open(filename, "r+") as f:
            self.berechnung = Berechnung.fromDict(json.loads(f.read()))
            print(self.berechnung)

    def writeToFile(self):
        with open(self.berechnung.filename, "w+") as f:
            f.write(json.dumps(self.berechnung.toDict(), indent=4))

    def fileSave(self):
        try:
            if self.berechnung.filename is None:
                self.berechnung.filename = QFileDialog.getSaveFileName()[0]
        except AttributeError:
            self.noProjectExecption()
        self.writeToFile()

    def fileSaveAs(self):
        try:
            self.berechnung.filename = QFileDialog.getSaveFileName()[0]
        except AttributeError:
            self.noProjectExecption()
        self.writeToFile()

    def newProject(self):
        self.npw = NewProjectWindow(self)

    def setProject(self, b):
        self.berechnung = b


class NewProjectWindow(QtWidgets.QWidget):
    def __init__(self, main):
        QWidget.__init__(self)
        self.resize(200, 175)
        self.main = main
        self.setWindowTitle("New Project")
        self.show()

        self.nametextfield = QLineEdit("Name des Projektes", self)
        self.nametextfield.setGeometry(QRect(5, 25, 190, 30))
        self.nametextfield.show()

        self.authortextfield = QLineEdit("Author des Projektes", self)
        self.authortextfield.setGeometry(QRect(5, 75, 190, 30))
        self.authortextfield.show()

        self.createbtn = QPushButton(self, text="create Project")
        self.createbtn.setGeometry(QRect(5, 125, 190, 40))
        self.createbtn.clicked.connect(self.createBerechnung)
        self.createbtn.show()

    def createBerechnung(self):
        self.main.setProject(
            Berechnung(
                name=self.nametextfield.text(),
                author=self.authortextfield.text()
            )
        )
        self.close()


if __name__ == "__main__":
    Core.QCoreApplication.setAttribute(Core.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrm()
    widget.show()

    sys.exit(app.exec())
