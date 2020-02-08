# coding=utf-8

Enoncé

« Devops » est une philosophie d’organisation au sein d’une DSI (Direction des systèmes d’information). Elle vise principalement à rapprocher les équipes de développement et les équipes d’exploitation sur le plan structurel et humain. Tout le cycle de vie d’un produit devient important, de sa conception aux retours des clients.

Depuis la mise en place de la culture « Devops », une entreprise cherche à mesurer la plus-value apportée à la satisfaction client.

Pour cela, un questionnaire de satisfaction est envoyé aux clients après chaque mise en production du produit. Le questionnaire permet de déterminer si le client est satisfait ou non. On attribue une note à chaque mise en production à l'aide de la formule suivante :- 10 si le nombre de clients satisfaits n’a pas changé
- 15 si le nombre de clients satisfaits a augmenté
- 20 si le nombre de clients satisfaits a augmenté pour la deuxième fois consécutive
- 5 si le nombre de clients satisfaits a baissé
- 0 si le nombre de clients satisfaits a baissé pour la deuxième fois consécutive
Vous devez déterminer la note moyenne de satisfaction client à la fin de l’année en considérant que le nombre de client satisfaits en début d'année est égal à 0.


Format des données

Entrée
Ligne 1 : un entier N représentant le nombre de mises en production durant l’année.
Ligne 2 à N+1 : un entier S correspondant au nombre de clients satisfaits.

Sortie
Un entier représentant la note moyenne arrondie à l'entier supérieur.

# ***************************************************************
# *
# *
# * SOLUTION BY Kibo
# *
# *
# ******************************************************************
# *******
# * Read input from STDIN
# * Use echo or print to output your result, use the /n constant at the end of each result line.
# * Use:
# *      local_print (variable );
# * to display simple variables in a dedicated area.
# * ***/
import sys
from math import ceil

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
n = int(lines[0])
lines = lines[1:]
local_print(lines);
precprec = 0
prec = 0
notes = []
for elem in lines:
    if prec == int(elem):
        notes.append(10)
    if int(elem) > prec:
        if prec > precprec:
            notes.append(20)
        else:
            notes.append(15)
    if int(elem) < prec:
        if prec < precprec:
            notes.append(0)
        else:
            notes.append(5)
    precprec = prec
    prec = int(elem)
som = 0
for note in notes:
    som += note

print(ceil(som / len(notes)))


