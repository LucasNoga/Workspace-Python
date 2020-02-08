Objectif

En attendant la neige, on peut toujours dessiner des flocons.... Le but de ce challenge est de dessiner des flocons.

Pour dessiner un flocon de taille N (où N est un entier impair), vous devez créer un losange de dimension N dans une feuille comprenant N lignes et N colonnes. Chaque point non compris dans le losange est représenté par un . et chaque point du losange est représenté par un *.

Exemples
Si N = 3, le losange sera ainsi :
.*.
***
.*.

Si N =7, le losange sera ainsi :
...*...
..***..
.*****.
*******
.*****.
..***..
...*...


Données

Entrée
Ligne 1 : un entier impair N compris entre 3 et 51 représentant la taille du flocon.

Sortie
N lignes de N caractères représentant le flocon. Chaque caractère pouvant être un . ou un *.
Si vous rencontrez des problèmes avec les sauts de ligne dans votre sortie, vous pouvez aussi renvoyer une ligne unique comprenant toutes les lignes du dessin, en séparant chaque ligne du dessin par un espace. Par exemple si N=3 votre sortie serait :
.*. *** .*.


##
## Solution by ISOGRAD
##
N = int(input())
middle = (N - 1) // 2
for i in range(N):
    s = ""
    for j in range(N):
        if (i <= middle and middle - i <= j <= middle + i) or (i > middle and i - middle <= j <= N - 1 + middle - i):
            s += "*"
        else:
            s += "."
    print(s)