from dataclasses import dataclass, field
from datetime import date, datetime
from dataclasses import field
from calendar import month_name as months


frmt = "%Y-%m-%d"

def createMonths():
    m = Month(0)
    return [m].append([Month(i, months[i]) for i in range(0, 13)])

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

    def getSteuern(self):
        return self.wert/(100+self.mwst)*self.mwst

    def getNetto(self):
        return self.wert / (100 + self.mwst) * 100


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
    monthly = None
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

    def getDifferenz(self) -> int:
        geldEinnahmen = 0
        for e in self.einnahmen:
            geldEinnahmen += e.wert

        geldAusgaben = 0
        for a in self.ausgaben:
            geldAusgaben += a.wert

        return geldEinnahmen - geldAusgaben


@dataclass
class Berechnung(object):
    name: str
    datum: date = date.today()
    author: str = "Kein Author"
    months: list[Month] = field(default_factory=createMonths())
    filename: str = None

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        newdict["months"] = [m.toDict() for m in self.months]
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        d["months"] = [Month.fromDict(m) for m in d["months"]]
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
