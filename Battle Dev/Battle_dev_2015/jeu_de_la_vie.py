Énoncé

Ce challenge est basé sur le jeu de la vie dont vous trouverez les principes ici : http://fr.wikipedia.org/wiki/Jeu_de_la_vie.

Dans cette variante, à chaque étape :- lorsqu'une cellule a une voisine vivante au-dessus et une voisine vivante à gauche : elle devient vivante ;
- lorsqu'une cellule n'a pas de voisine vivante ni au-dessus ni à gauche : elle meurt ;
- dans le reste des cas, elle conserve son état.
Vous devez indiquer le temps de survie de la population à partir d'une configuration initiale. C'est à dire le nombre d'étapes après lequel il n'y a plus de cellule vivante.

Par commodité, la configuration initiale sera décrite par une série de rectangles de cellules vivantes.

Format des données

Entrée

Ligne 1 : un entier N compris entre 1 et 1 000 représentant le nombre de rectangles.
Lignes 2 à N+1 : quatre nombres entiers x1 y1 x2 y2 chacun compris entre 1 et 1 000 000 et séparés par des espaces. Touts les points inclus dans le rectangle délimité par x1, y1 (coin haut-gauche) et x2, y2 (coin bas-droite) sont des cellules vivantes. En effet, les abscisses vont croissant vers la droite, et les ordonnées vont croissant vers le bas.

Il n'y aura pas plus de 1 000 000 de cellules vivantes au départ.

Sortie
Un entier représentant le temps de survie de la population. Si la population survit indéfiniment, renvoyez -1.

Exemple



Cette génération, désignée sur l'image tout à gauche par le test de 3 rectangles suivant :

3
5 1 5 1
2 2 4 2
2 3 2 4

a une durée de vie de 6.



#*****
#Solution by ISOGRAD
#*****

class UnionFind:
    def __init__(self, n):
        self.pere = list(range(n))
        self.rang = [0] * n

    def find(self, x):
        if self.pere[x] == x:
            return x
        else:
            repr_x = self.find(self.pere[x])
            self.pere[x] = repr_x
            return repr_x

    def union(self, x, y):
        repr_x = self.find(x)
        repr_y = self.find(y)
        if repr_x == repr_y:
            return False
        if self.rang[repr_x] == self.rang[repr_y]:
            self.rang[repr_x] += 1
            self.pere[repr_y] = repr_x
        elif self.rang[repr_x] > self.rang[repr_y]:
            self.pere[repr_y] = repr_x
        else:
            self.pere[repr_x] = repr_y
        return True

T = 1
for t in range(T):
    N = int(input())
    uf = UnionFind(N)
    max_x = [0] * N
    max_y = [0] * N
    min_c = [0] * N
    rectangles = []
    for i in range(N):
        x1, y1, x2, y2 = map(int, input().split())
        max_x[i] = x2
        max_y[i] = y2
        min_c[i] = x1 + y1
        for j in range(i):
            x1a, y1a, x2a, y2a = rectangles[j]
            if not (x2a + 1 < x1 or x2 + 1 < x1a or y2a + 1 < y1 or y2 + 1 < y1a) and not (x2a + 1 == x1 and y2a + 1 == y1) and not (x2 + 1 == x1a and y2 + 1 == y1a):
                ii = uf.find(i)
                jj = uf.find(j)
                uf.union(i, j)
                k = uf.find(i)
                max_x[k] = max([max_x[k], max_x[ii], max_x[jj]])
                max_y[k] = max([max_y[k], max_y[ii], max_y[jj]])
                min_c[k] = min([min_c[k], min_c[ii], min_c[jj]])
        rectangles.append((x1, y1, x2, y2))
    lifespan = 0
    for i in range(N):
        k = uf.find(i)
        if max_x[k] + max_y[k] - min_c[k] + 1 > lifespan:
            lifespan = max_x[k] + max_y[k] - min_c[k] + 1
    print(lifespan)


