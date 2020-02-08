# coding=utf-8
Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/salesforcebuilding.pdf

Enoncé

Pour organiser l'agencement des nouveaux bureaux de SalesForce, vous devez regrouper les équipes par étage. Tous les étages doivent contenir le même nombre de personnes. Par contre, vous avez deux contraintes : - Vous pouvez placer au plus 2 équipes par étage.
- Une équipe doit être entièrement hébergée sur un étage (vous ne pouvez pas installer une partie d'une équipe sur un étage).
On vous donne le nombre de collaborateurs des différentes équipes qui peuvent potentiellement être installées dans l'immeuble. Le but de ce challenge est de déterminer combien d'étages vous pouvez remplir intégralement (c'est à dire sans laisser aucune place vide). Il est très probable que votre résultat aboutisse à ce que certaines équipes ne soient pas installées dans cet immeuble.

Pour simplifier, il n'y a pas de limite sur le nombre d'étages.

Format des données

Entrée

Ligne 1 : un entier L compris entre 5 et 100 représentant le nombre de places que vous devez remplir sur chaque étage.
Ligne 2 : un entier N compris entre 10 et 500 représentant le nombre d'équipes qui peuvent être potentiellement installées dans l'immeuble.
Lignes 3 à N+2 : un entier compris entre 1 et 50 représentant le nombre de collaborateurs d'une équipe.

Sortie
Un entier représentant le nombre d'étages que vous pouvez intégralement remplir avec L collaborateurs en respectant les contraintes exprimées dans l'énoncé : pas plus de deux équipes par étage et impossibilité d'installer seulement une partie d'une équipe sur un étage.



l = int(input())
n = int(input())
t = [0 for i in range(200)]
# Astuce : on a une grosse reserve de briques de longueur 0,
# comme ca les murs a 1 brique sont des cas particuliers de murs a 2 briques
t[0] = n
for i in range(n):
    x = int(input())
    t[x] += 1

c = 0
x = 0
while x < l - x:
    c += min(t[x], t[l-x])
    x += 1
if x == l - x:
    c += t[x] // 2

print(c)

