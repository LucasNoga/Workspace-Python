# coding=utf-8
Enoncé

Une « blockchain » est une technologie de stockage numérique et de transmission à coût minime, décentralisée, et totalement sécurisée.

Dans cette question, nous allons simplifier ce concept en comparant une « blockchain » à un livre que vous allez devoir mettre à jour. Ce livre est stocké chez plusieurs personnes à la fois. N'importe qui peut demander à écrire une lettre de l'alphabet dans ce livre (y compris des personnes ne stockant pas le livre chez eux).

Néanmoins, pour que la demande d'écriture soit validée, il faut qu'au minimum la moitié des personnes stockant le livre soit d'accord pour ajouter cette écriture. Si la demande obtient la majorité, le livre se met à jour automatiquement partout où il est stocké. Sinon le livre reste tel quel.

On considère que le livre est initialement vide.


Format des données

Entrée
Ligne 1 : un entier P correspondant au nombre de personnes stockant le livre
Ligne 2 : un entier N correspondant au nombre de demandes d'écriture
Ligne 3 à N+2 : une lettre de l'alphabet C et un entier Q séparés par un espace où C est la demande d'écriture et Q le nombre de personne ayant validé cette demande.

Sortie
Une chaîne de caractères représentant le contenu du livre.

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

lines = []
chaine = ""
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
p = int(lines[0])
n = lines[1]
lines = lines[2:]
for ligne in lines:
    c, q = ligne.split(" ")
    if int(q) >= p / 2:
        chaine += c

print(chaine)


