# Énoncé
#
# Dans ce challenge, vous devez déterminer le nombre de personnes situées dans une zone rectangulaire. Les coordonnées des personnes et de la zone sont fournies sous forme de latitude et de longitude.
#
# Format des données
#
# Entrée
# Ligne 1 : quatre nombres flottants from_lat, from_lng, to_lat et to_lng tous compris entre 0 et 51 utilisant le "." comme séparateur décimal et séparés par des espaces, indiquant respectivement la latitude minimale, la longitude minimale, la latitude maximale et la longitude maximale de la zone rectangulaire à contrôler.
# Ligne 2 : un entier N représentant le nombre de personnes géolocalisées.
# Lignes 3 à N+2 : deux nombres flottants lat et lng utilisant le "." comme séparateur décimal et séparés par un espace représentant les coordonnées d'une personne géolocalisée.
#
# Sortie
# Un entier représentant le nombre de personnes se trouvant dans la zone à contrôler (les bords sont inclus).

import numpy as np

lines = open("/home/admin/Documents/trainBattleDev/ex2/input1.txt", "r").read()

print(lines)

data = lines.split()
print(type(data[0]))
coordsBox = data[0:4]
print(coordsBox)
nbPeople = data[4]
print(nbPeople)
coordsPeople = data[5:]

Xcoords = []
Ycoords = []
for i in np.arange(0, len(coordsPeople) - 1, 2):
    Xcoords.append(coordsPeople[i])
    Ycoords.append(coordsPeople[i + 1])

personInBox = 0
XgoodCoords = False
YgoodCoords = False

for i, coords in enumerate(Xcoords):
    if coordsBox[0] < Xcoords[i] < coordsBox[2]:
        XgoodCoords = True
    else:
        XgoodCoords = False
    if coordsBox[1] < Ycoords[i] < coordsBox[3]:
        YgoodCoords = True
    else:
        YgoodCoords = False
    if XgoodCoords == True and YgoodCoords == True:
        personInBox += 1

print("Le nombre de personnes dans la boite est : ", personInBox)

