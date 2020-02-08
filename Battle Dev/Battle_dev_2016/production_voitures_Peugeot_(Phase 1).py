Enoncé

Dans ce challenge, l'objectif est de déterminer la production d'une usine Peugeot sur un mois.

Chaque jour, l'usine produit un nombre de voitures X.

Votre code doit renvoyer le nombre de voitures produites durant un mois.

Format des données

Entrée
Ligne 1 : un entier N entre 28 et 31 représentant le nombre de jours dans le mois.
Ligne 2 à N+1 : un entier X entre 10 et 100 représentant le nombre de voitures produites un jour du mois. Il y a une ligne pour chaque jour.

Sortie
Un entier indiquant le nombre de voitures produites durant le mois


import sys

n = int(input())
print(sum(int(input()) for _ in range(n)))