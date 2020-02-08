# coding=utf-8
Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/dodecagon.pdf

Objectif

En mathématiques, un Dodécagone est un polygone avec 12 côtés. On va ici considérer des dodécagones de dimension P (avec P un entier impair) sur une grille de dimension NxN (avec N un entier impair), que l'on va construire en remplissant un carré centré sur le milieu de la grille et en enlevant les 4 coins. Par exemple si N = 7, on peut dessiner les dodécagones suivants :



L'objectif de ce challenge est de dessiner des "dodécagones empilés" de couleurs alternées. Vos dodécagones auront toujours une taille impaire supérieure ou égale à 3.

Exemple

Si on empile les 3 dodécagones ci-dessus du plus grand au plus petit, on obtient la figure suivante :



Données

Entrée
Ligne 1 : un entier impair N compris entre 5 et 51 représentant la taille de la grille.

Sortie
N lignes comprenant N caractères représentant la grille avec les dodécagones empilés. Les dodécagones empilés sont de dimension N, N-2, ..., jusqu'à 3. Le plus grand est situé en dessous. Les cases vides sont représentées par le caractère . et les dodécagones sont remplis alternativement de caractères * et #. Le plus grand est rempli de caractères *, puis le suivant est rempli de caractères #, puis le suivant de caractères * et ainsi de suite.

Si vous rencontrez des problèmes avec les sauts de ligne dans votre sortie, vous pouvez aussi renvoyer une ligne unique comprenant toutes les lignes du dessin, en séparant chaque ligne du dessin par un espace. Par exemple si N=5 votre sortie serait :
.***. **#** *###* **#** .***.



#*
#* SOLUTION by ISOGRAD
#*
n = int(input())

t = [['.' for j in range(n)] for i in range(n)]

m = n // 2

for i in range(n):
    for j in range(n):
        x = abs(i - m)
        y = abs(j - m)
        d = max(x,y)
        if x == y:
            d += 1
        if d % 2 == m % 2:
            t[i][j] = '*'
        else:
            t[i][j] = '#'

t[0][0] = '.'
t[0][n-1] = '.'
t[n-1][0] = '.'
t[n-1][n-1] = '.'
t[m][m] = t[m][m-1]

for l in t:
    print("".join(l))

