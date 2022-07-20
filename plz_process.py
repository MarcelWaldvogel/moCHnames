#!/usr/bin/python3
# Creates a PLZ->(Shortest_Name, Canton) map as a JavaScript file
# The shortest name is chosen as this probably will be the one without extras
import csv
import json

plzmap = {}
# There are some very long lines (due to the coordinates)
csv.field_size_limit(222000)
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

# Sort them in ascending order by PLZ
sortedmap = {}
for plz in sorted(plzmap.keys()):
    sortedmap[plz] = plzmap[plz]

with open("data/plz.json", "w") as out:
    json.dump(sortedmap, out)
