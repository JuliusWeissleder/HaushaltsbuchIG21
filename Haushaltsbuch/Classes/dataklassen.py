from dataclasses import dataclass, field
from datetime import date, datetime
from calendar import month_name as ms

frmt = "%Y-%m-%d"


def createMonths():
    m = Month(0)
    return [m].__add__([Month(i, ms[i], m) for i in range(1, 13)])


def sort(ltosort, key: str):
    unsorteddict = {a.__dict__[key]: [] for a in ltosort if a.__dict__[key] is not None}
    for a in ltosort:
        if a.__dict__[key] is not None:
            unsorteddict[a.__dict__[key]].append(a)
    sortedlist = []
    for l in [unsorteddict[k] for k in sorted(unsorteddict.keys())]:
        sortedlist.append(l)
    return sortedlist


@dataclass
class Ausgabe(object):
    wert: float
    mwst: int
    katagorie: str
    artikel: str
    datum: date = date.today()
    menge: int = None

    def getSteuern(self):
        return self.wert/(100+self.mwst)*self.mwst

    def getNetto(self):
        return self.wert / (100 + self.mwst) * 100

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        return Ausgabe(**d)


@dataclass
class Einahme(object):
    wert: float
    katagorie: str
    datum: date = date.today()

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        return Einahme(**d)


class Month(object):
    pass


@dataclass
class Month(object):
    id: int 
    name: str = "Monthly"
    monthly: Month = None
    einnahmen: list[Einahme] = field(default_factory=list)
    ausgaben: list[Ausgabe] = field(default_factory=list)

    def getDifferenz(self) -> int:
        geldEinnahmen = 0
        for e in self.einnahmen:
            geldEinnahmen += e.wert
        geldAusgaben = 0
        for a in self.ausgaben:
            geldAusgaben += a.wert
        if self.monthly is None:
            return geldEinnahmen - geldAusgaben
        else:
            return self.monthly.getDifferenz() + geldEinnahmen - geldAusgaben

    def getSortedAusgabenBy(self, key: str):
        return sort(self.ausgaben, key)

    def getSortedEinnahmenBy(self, key: str):
        return sort(self.einnahmen, key)

    def addEinahme(self, e: Einahme):
        self.einnahmen.append(e)

    def addAusgabe(self, a: Ausgabe):
        self.ausgaben.append(a)

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
    months: list[Month] = field(default_factory=createMonths)
    filename: str = None

    def addEinahme(self, e: Einahme):
        self.months[e.datum.month].addEinahme(e)

    def addAusgabe(self, a: Ausgabe):
        self.months[a.datum.month].addAusgabe(a)

    def getDifferenz(self) -> int:
        differenz = 0
        for m in [m for m in self.months if 0 != m.id]:
            differenz += m.getDifferenz()
        return differenz

    def toDict(self):
        newdict = self.__dict__.copy()
        newdict["datum"] = self.datum.strftime(frmt)
        newdict["months"] = [m.toDict() for m in self.months]
        return newdict

    def fromDict(d: dict):
        d["datum"] = datetime.strptime(d["datum"], frmt).date()
        d["months"] = [Month.fromDict(m) for m in d["months"]]
        return Berechnung(**d)
