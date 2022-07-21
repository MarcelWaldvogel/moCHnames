#!/usr/bin/python3
# Creates a PLZ->(Shortest_Name, Canton) map as a JavaScript file
# The shortest name is chosen as this probably will be the one without extras
import csv
import json

###
# Input first, last, and PLZ
###

# First names
vormap = {}
with open("raw/vornamen_proplz.csv", "r", newline="") as vorfile:
    vors = csv.DictReader(vorfile, delimiter=';')
    for vorline in vors:
        plz = vorline['PLZ']
        name = vorline['Vorname']
        sex = vorline['Geschlecht']
        if name != "n/a":
            if plz in vormap:
                if sex == "m":
                    vormap[plz]["m"].append(name)
                else:
                    vormap[plz]["f"].append(name)
            else:
                if sex == "m":
                    vormap[plz] = {"m": [name], "f": []}
                else:
                    vormap[plz] = {"m": [], "f": [name]}

# Last names
nachmap = {}
with open("raw/nachnamen_proplz.csv", "r", newline="") as nachfile:
    nachs = csv.DictReader(nachfile, delimiter=';')
    for nachline in nachs:
        plz = nachline['PLZ']
        name = nachline['Nachname']
        sex = nachline['Geschlecht']
        if name != "n/a":
            if plz in nachmap:
                if sex == "m":
                    nachmap[plz]["m"].append(name)
                else:
                    nachmap[plz]["f"].append(name)
            else:
                if sex == "m":
                    nachmap[plz] = {"m": [name], "f": []}
                else:
                    nachmap[plz] = {"m": [], "f": [name]}


# Postal codes
# There are some very long lines (due to the coordinates)
csv.field_size_limit(222000)
plzmap = {}
with open("raw/plz_verzeichnis_v2.csv", "r", newline="") as plzfile:
    plzs = csv.DictReader(plzfile, delimiter=';')
    for plzline in plzs:
        plz = plzline['POSTLEITZAHL']
        ort = plzline['ORTBEZ18']
        kanton = plzline['KANTON']
        if plz in plzmap:
            if len(ort) < len(plzmap[plz][0]):
                plzmap[plz] = (ort, kanton)
        else:
            plzmap[plz] = (ort, kanton)

###
# Output PLZ to city, and name maps
###

# Sort PLZ in ascending order by PLZ
sortedmap = {}
for plz in sorted(plzmap.keys()):
    sortedmap[plz] = plzmap[plz]

with open("src/data/plz.json", "w") as out:
    json.dump(sortedmap, out, separators=(',', ':'))

# Sort names in ascending order by PLZ; and output only those with both name parts for women and men
sortedmap = {}
for plz in sorted(vormap.keys()):
    if (plz in nachmap and plz in plzmap and
        len(vormap[plz]['m']) > 0 and len(vormap[plz]['f']) > 0 and
            len(nachmap[plz]['m']) > 0 and len(nachmap[plz]['f']) > 0):
        sortedmap[plz] = {"m": [vormap[plz]["m"], nachmap[plz]["m"]],
                          "f": [vormap[plz]["f"], nachmap[plz]["f"]],
                          "l": plzmap[plz][0], 'c': plzmap[plz][1]}

with open("src/data/name.json", "w") as out:
    json.dump(sortedmap, out, separators=(',', ':'))
