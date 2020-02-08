# coding=utf-8

Enoncé

Le « cloud computing » est un modèle qui permet un accès pratique et à la demande à un ensemble de ressources informatiques. Ce modèle est très apprécié par les entreprises car il leur permet d'accéder à une multitude de ressources informatiques tout en ne possédant aucune machine physique dans leurs locaux.

Un hébergeur est une entité qui possède des serveurs et les met à disposition des entreprises. Un serveur a un coût en électricité et en maintenance. L'objectif pour cette entité est d'optimiser le nombre de serveurs allumés. Il faut en avoir suffisamment pour répondre aux besoins de ses clients sans jamais en avoir trop pour ne pas gaspiller d'argent.

On considère que la journée est divisée en quatre parties:- le matin de 05:30 à 11:59
- l'après-midi de 12:00 à 17:59
- le soir de 18:00 à 23:29
- la nuit de 23:30 à 05:29
Un hébergeur souhaite connaitre la période de la journée où il y a le plus grand nombre de demandes de serveurs.

On vous garantit qu'il n'y a qu'une seule période de la journée où l'hébergeur est le plus sollicité.

Format des données

Entrée
Ligne 1 : un entier N représentant le nombre de demandes de serveurs dans une journée
Ligne 2 à N+1 : une heure H au format HH:MM correspondant à une heure de demande.

Sortie
Une chaîne de caractères :- M si l'hébergeur est plus sollicité le matin
-AM si l'hébergeur est plus sollicité l'après-midi
-S si l'hébergeur est plus sollicité le soir
-N si le cloud est plus sollicité la nuit

# ***************************************************************
# *
# *
# * SOLUTION BY Kibo
# *
# *
# ******************************************************************
import sys

lines = []
valeur = {"M": 0, "AM": 0, "S": 0, "N": 0}
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
n = lines[0]
lines = lines[1:]
for h in lines:
    heure, minute = h.split(":")
    if (int(heure) == 5 and int(minute) >= 30) or 6 <= int(heure) <= 11:
        valeur["M"] += 1
    if int(heure) <= 17 and int(heure) >= 12:
        valeur["AM"] += 1
    if (int(heure) == 23 and int(minute) <= 29) or 18 <= int(heure) <= 22:
        valeur["S"] += 1
    if (int(heure) == 23 and int(minute) >= 30) or (int(heure) == 5 and int(minute) <= 29) or 23 <= int(heure) <= 4:
        valeur["N"] += 1

    if h in valeur.keys():
        valeur[h] += 1
    else:
        valeur[h] = 1
max = 0
maxkey = ""
for key, value in valeur.items():
    if max < value:
        max = value
        maxkey = key
print(maxkey)

