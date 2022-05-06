from dataclasses import dataclass
from datetime import date, datetime
from dataclasses import field


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
class Berechnung(object):
    name: str
    datum: date = date.today()
    author: str = "Kein Author"
    einnahmen: list[Einahme] = field(default_factory=list)
    ausgaben: list[Ausgabe] = field(default_factory=list)

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        newdict["einnahmen"] = [e.toDict() for e in self.einnahmen]
        newdict["ausgaben"] = [e.toDict() for e in self.ausgaben]
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        d["einnahmen"] = [Einahme.fromDict(e) for e in d["einnahmen"]]
        d["ausgaben"] = [Ausgabe.fromDict(e) for e in d["ausgaben"]]
        return Berechnung(**d)

    def addEinahme(self, e: Einahme):
        self.einnahmen.append(e)

    def getEinnahme(self):
        return self.einnahmen

    def addAusgabe(self, a: Ausgabe):
        self.ausgabesn.append(a)

    def getAusgaben(self):
        return self.ausgaben