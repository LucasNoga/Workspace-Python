# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/kayak2.pdf

Objectif

On considère une épreuve de slalom en kayak se déroulant dans un bassin artificiel d'eau vive de forme carrée. L'épreuve consiste à se diriger d'un coin du bassin à l'opposé, l'eau étant mue par un courant puissant allant dans cette direction. Cela dit, il ne s'agit pas simplement de se laisser emporter par le courant : des portes sont disposées dans le bassin et l'objectif est d'en franchir le plus possible durant son parcours.

Le bassin est représenté par une grille de taille NxN. La case de départ est le coin en haut à gauche, et l'arrivée est le coin en bas à droite. Comme il est difficile d'aller à contre-courant, la direction du courant étant vers le bas-droite, les seuls déplacements possibles sont, à partir d'une case, d'aller vers la case en bas, la case à droite, ou la case en diagonale en bas à droite.

Pour passer une porte, il suffit de passer sur le case où se trouve la porte. Il n'y a pas de sens de passage.

La grille pouvant être très grande, une solution en force brutale ne fonctionnera pas et un algorithme d'une complexité aux alentours de O(N^2) est attendue.


Données

Entrée

Ligne 1 : un entier N compris entre 5 et 1000, représentant la taille de la grille.
Lignes 2 à N+1 : les lignes de la carte représentées par des chaînes de N caractères. Les caractères de la ligne sont soit X (une porte), soit . (vide).


Sortie

Un entier, représentant le nombre maximal de portes qu'un ou une kayakiste peut franchir au long de son parcours entre la case de départ et la case d'arrivée.



n = int(input())
t = [input() for i in range(n)]

c = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
    for j in range(n):
        if i > 0:
            c[i][j] = max(c[i][j], c[i-1][j])
        if j > 0:
            c[i][j] = max(c[i][j], c[i][j-1])
        if t[i][j] == 'X':
            c[i][j] += 1

print(c[n-1][n-1])
