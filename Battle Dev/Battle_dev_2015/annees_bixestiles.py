Énoncé

Le but de challenge est de déterminer si une année est bissextile ou non.
Comme indiqué ici : http://fr.wikipedia.org/wiki/Année_bissextile, depuis l'ajustement du calendrier grégorien, sont bissextiles les années :- soit divisibles par 4 mais non divisibles par 100 ;
- soit divisibles par 400.
Format des données

Entrée
Ligne 1 : un entier N représentant le nombre d'années à considérer.
Lignes 2 à N+1 : un entier compris entre 1582 et 2048 représentant une année.

Sortie
Vous devez afficher N lignes correspondant aux N années du fichier d'entrée. Avec sur chaque ligne, la chaîne BISSEXTILE si l'année est bissextile, NON BISSEXTILE sinon.

# *****
# Solution de Chewb
# **/

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

for i, l in enumerate(lines):
    if i != 0:
        y = int(l)
        if y % 4 == 0 and y % 100 != 0:
            print("BISSEXTILE")
        elif y % 400 == 0:
            print("BISSEXTILE")
        else:
            print("NON BISSEXTILE")


