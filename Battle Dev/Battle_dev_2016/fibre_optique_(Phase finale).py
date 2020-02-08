Énoncé

Vous avez entre vos mains la carte du nouveau parc informatique de votre entreprise. On vous demande de relier tous ordinateurs dans un même réseau local. Mais la fibre optique coûte cher, donc vous devez utiliser le moins de fibre possible.

À partir des positions dans le plan des ordinateurs, vous devez calculer la longueur de fibre optique minimale requise pour tous les relier.

Exemple

Pour la configuration suivante, il faut au moins une longueur de fibre optique de 2 + 4 * sqrt(2) soit environ 7.657, pour relier tous les ordinateurs.



Format des données

Entrée
Ligne 1 : un entier N compris entre 1 et 200, représentant le nombre d'ordinateurs du parc informatique.
Lignes 2 à N+1 : deux entiers X et Y compris entre 1 et 1000 et séparés par un espace indiquant respectivement l'abscisse et l'ordonnée d'un ordinateur à relier.

Il n'y aura jamais 2 ordinateurs à la même position.

Sortie
Un nombre décimal utilisant le "." comme séparateur, représentant la longueur minimale de fibre optique pour relier tous les ordinateurs en réseau, arrondie à 3 chiffres après la virgule. Votre réponse sera acceptée avec une tolérance de 1/1000.


#*******************Solution by TurpIF ******************/
n = int(input())
P = {tuple(map(int, input().split())) for _ in range(n)}
d = 0

import math

root = next(iter(P))
S = set([root])
D = dict()
N = dict()
for p in P - S:
    N[p] = root
    D[p] = math.sqrt((p[0] - root[0]) ** 2 + (p[1] - root[1]) ** 2)
local_print(D)

while len(S) != len(P):
    Min, Dist = min(D.items(), key=lambda x: x[1])
    local_print(str(Min) + " " + str(Dist))
    d += Dist
    del D[Min]
    S.add(Min)
    for p in P - S:
        newD = math.sqrt((p[0] - Min[0]) ** 2 + (p[1] - Min[1]) ** 2)
        if D[p] > newD:
            N[p] = Min
            D[p] = newD
print(d)