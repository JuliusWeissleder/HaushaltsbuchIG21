from dataclasses import dataclass, field
from datetime import date, datetime
from dataclasses import fiel
from calendar import month_name as months


frmt = "%Y-%m-%d"


def simple(o):
    return type(o) in [type(str()), type(int()), type(float()), type(bool()), type(None)]

@dataclass
class Ausgabe(object):
    wert: int
    mwst: str
    katagorie: str
    artikel: str
    name: str = None
    menge: int = None
    datum: date = date.today()

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        return Ausgabe(**d)

@dataclass
class Einahme(object):
    wert: int
    katagorie: str
    name: str = None
    datum: date = date.today()

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        return Einahme(**d)


@dataclass
class Month(object):
    id: int 
    name: str = "Monthly"
    einnahmen: list[Einahme] = field(default_factory=list)
    ausgaben: list[Ausgabe] = field(default_factory=list)

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["einnahmen"] = [e.toDict() for e in self.einnahmen]
        newdict["ausgaben"] = [e.toDict() for e in self.ausgaben]
        return newdict

    def fromDict(d: dict):
        d["einnahmen"] = [Einahme.fromDict(e) for e in d["einnahmen"]]
        d["ausgaben"] = [Ausgabe.fromDict(e) for e in d["ausgaben"]]
        return Month(**d)

@dataclass
class Berechnung(object):
    name: str
    datum: date = date.today()
    author: str = "Kein Author"
    months: list[Month] = field(default_factory=list)
    filename: str = None

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        newdict["months"] = [m.toDict() for m in self.months]
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        d["einnahmen"] = [Month.fromDict(m) for m in d["months"]]
        return Berechnung(**d)

    def addEinahme(self, e: Einahme):
        self.einnahmen.append(e)

    def addAusgabe(self, a: Ausgabe):
        self.ausgaben.append(a)

    def getDifferenz(self) -> int:
        geldEinnahmen = 0
        for e in self.einnahmen:
            geldEinnahmen += e.wert

        geldAusgaben = 0
        for a in self.ausgaben:
            geldAusgaben += a.wert

        return geldEinnahmen - geldAusgaben

    def createMonths():
        return [Month(i, months[i]) for i in range(0, 13)]
