# coding=utf-8
Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/iterativekayak2.pdf

Objectif

Cette fois-ci, on reprend l'épreuve précédente en modifiant légèrement les règles : au lieu d'effectuer un seul parcours, on en réalise autant qu'il en faut pour avoir traversé chaque porte au moins une fois. À chaque fois qu'on franchit une porte, celle-ci s'active et reste activée jusqu'à la fin de l'épreuve. Au départ, aucune porte n'est activée, et il faut recommencer le parcours jusqu'à ce que toutes les portes s'activent ; à ce moment, l'épreuve s'arrête. Le but est d'activer toutes les portes en effectuant le nombre minimal de parcours.

Pour rappel, le bassin est représenté par une grille de taille NxN. La case de départ est le coin en haut à gauche, et l'arrivée est le coin en bas à droite. Comme il est difficile d'aller à contre-courant, la direction du courant étant bas-droite, les seuls déplacements possibles sont, à partir d'une case, d'aller vers la case en bas, la case à droite, ou la case en diagonale en bas à droite. Les portes sont marquées comme des cases spécifiques sur la grille ; le sens de franchissement d'une porte n'a aucune importance.

Une solution en temps polynomial, c'est à dire une complexité O(N^k), est attendue.

Données

Entrée

Ligne 1 : un entier N compris entre 5 et 50, représentant la taille de la grille.
Lignes 2 à N+1 : les lignes de la carte représentées par des chaînes de N caractères. Les caractères de la ligne sont soit X (une porte), soit . (vide).

Sortie

Un entier, représentant le nombre minimal de parcours dont un ou une kayakiste a besoin pour franchir chaque porte au moins une fois.


# Bipartite matching taken from
# https://github.com/jilljenn/tryalgo/blob/master/tryalgo/bipartite_matching.py

def augment(u, bigraph, visit, match):
    for v in bigraph[u]:
        if not visit[v]:
            visit[v] = True
            if match[v] is None or augment(match[v],  bigraph, visit, match):
                match[v] = u
                return True
    return False


def max_bipartite_matching(bigraph):
    n = len(bigraph)
    match = [None] * n
    for u in range(n):
        augment(u, bigraph, [False] * n, match)
    return match

# end matching code

n = int(input())
t = [input() for i in range(n)]

V = []
for x in range(n):
    for y in range(n):
        if t[x][y] == 'X':
            V.append((x,y))
m = len(V)
bigraph = [[] for i in range(m)]
for i in range(m):
    for j in range(m):
        (xi,yi) = V[i]
        (xj,yj) = V[j]
        if i != j and xi <= xj and yi <= yj:
            bigraph[i].append(j)

matching = max_bipartite_matching(bigraph)
print (len([v for v in matching if v is None]))
