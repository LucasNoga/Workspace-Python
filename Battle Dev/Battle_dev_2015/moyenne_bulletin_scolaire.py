Enoncé

C'est la fin de l'année scolaire, moment fatidique du bulletin, il faut calculer les moyennes. Tous les élèves se ruent vers vous et vous supplient de calculer leur moyenne à leur place.
Facile ! Vous décidez d’écrire un script.

Format des données

Entrée
Ligne 1 : un entier N entre 20 et 100 représentant le nombre de notes.
Lignes 2 à N+1 : un entier compris entre 0 et 20 représentant une note.

Sortie
Un entier indiquant la moyenne générale de l'élève (arrondie à l'entier inférieur).


import math
N = int(input())
l = []
for _ in range(N):
    l.append(int(input()))
print(math.trunc(sum(l) / N))
