from dataklassen import Berechnung, Month, Ausgabe, createMonths
from dataclasses import dataclass, field
import random

rstr = """generation
worm
bomber
shake
prevent
owner
pray
practical
negative
tidy
examination
abstract
species
native
vertical
acid
smell
sausage
guard
unlikely"""
rstr = rstr.split("\n")

b = Berechnung("Test", author="ich")

for a in [Ausgabe(i, 19, random.choice(rstr), "s") for i in range(10)]:
    b.addAusgabe(a)
print(b.months[5].getSortedAusgabenBy("katagorie"))
print(b.getDifferenz())


