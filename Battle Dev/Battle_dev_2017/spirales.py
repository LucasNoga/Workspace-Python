# coding=utf-8
Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/spiral.pdf

Objectif

En mathématiques, une spirale est une courbe qui commence en un point central puis s'en éloigne de plus en plus, en même temps qu'elle tourne autour.

Dans ce challenge, notre spirale est uniquement composée de bords horizontaux et verticaux. Elle tourne dans le sens inverse des aiguilles d'une montre. Deux points de la spirale ne doivent jamais se toucher diagonalement. Un point situé sur un bord horizontal ne doit pas être au contact d'un point situé sur un autre bord horizontal. De même un point situé sur un bord vertical ne doit pas être au contact d'un point situé sur un autre bord vertical.

Le but de ce challenge est de dessiner une spirale de longueur maximale sur une grille comprenant N lignes et N colonnes (où N est un entier impair), en plaçant le premier point au centre et le second point à gauche du centre. Pour cela, vous devez tourner à gauche à chaque fois que cela est possible tout en respectant les contraintes ci-dessus et sans sortir de la feuille.

Exemples
Tout cela peut sembler un peu complexe, mais c'est plus clair avec des dessins.



Données

Entrée
Ligne 1 : un entier impair N compris entre 3 et 50 représentant la taille de la spirale (et la taille de la grille).

Sortie
N lignes de N caractères représentant la spirale. Chaque caractère peut être un = pour une case vide ou un # pour point de la spirale.
Si vous rencontrez des problèmes avec les sauts de ligne dans votre sortie, vous pouvez aussi renvoyer une ligne unique comprenant toutes les lignes du dessin, en séparant chaque ligne du dessin par un espace. Par exemple si N=3 votre sortie serait :
=== ##= #==




n = int(input())

t = [['=' for j in range(n)] for i in range(n)]

m = (n-1)//2
x = m
y = m

dxmod = [0, -1, 0, 1]
dymod = [-1, 0, 1, 0]

bound = n if n % 4 == 1 else n-1

for k in range(1,bound+1):
    dx = dxmod[k % 4]
    dy = dymod[k % 4]
    for i in range(k):
        t[y + i*dy][x + i*dx] = '#'
    x += k*dx
    y += k*dy

for l in t:
    print("".join(l))

