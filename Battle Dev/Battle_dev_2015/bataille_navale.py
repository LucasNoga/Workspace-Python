Énoncé

L'objet de ce challenge est de simuler un jeu de bataille navale. Pour cela vous devez d'abord identifier les bateaux sur une carte puis déterminer s'ils sont touchés ou coulés par une série de tirs.



Un bateau est un ensemble de points consécutifs horizontaux ou verticaux représentés par des # sur la carte. Pour éviter les ambigüités, aucune extrémité de bateau ne sera située à côté (horizontalement ou verticalement) d'un point d'un autre bateau. En d'autre mots, les situations comme celles en rouge ci-dessus ne seront jamais présentes dans les cartes.

Un bateau est touché s'il reçoit au moins un tir. Il est coulé s'il reçoit un tir sur chacun des points qui le composent.

Format des données

Entrée

Ligne 1 : trois entiers M, N et P séparés par des espaces où M et N sont les dimensions de la carte et P le nombre de missiles envoyés.
Lignes 2 à M+1: une chaîne de N caractères représentant une ligne de la carte. Un . représente de l'eau et un # représente une partie (ou l'intégralité) du bateau.
Lignes M+2 à M+P+1 : 2 entiers séparés par un espace représentant le numéro de la ligne et de la colonne du tir. La première ligne et la première colonne de la carte ont pour indice 0.

Sortie

2 entiers C et T séparés par un espace : C représente le nombre de bateaux coulés et T représente le nombre de bateaux touchés.


#*****
# Solution de ZomZom
#**/

#!/usr/bin/env python3

def analyse(g, M, N):
    C = 0
    T = 0

    lb = []
    for i in range(M):
        for j in range(N):
            if g[i][j] != '.':
                cb = []

                for k in range(j, N):
                    if g[i][k] != '.':
                        cb.append(g[i][k])

                    if g[i][k] == '.' or k == N-1:
                        if len(cb) > 1:
                            lb.append(cb)

                            for l in range(j, k+1):
                                grid[i][l] = '.'
                        break



    for j in range(N):
        for i in range(M):
            if g[i][j] != '.':
                cb = []
                for k in range(i, M):
                    if g[k][j] != '.':
                        cb.append(g[k][j])

                    if g[k][j] == '.' or k == M-1:
                        if len(cb) > 1:
                            lb.append(cb)

                            for l in range(i, k+1):
                                grid[l][j] = '.'
                        break

                    cb.append(g[k][j])

    for i in range(N):
        for j in range(M):
            if g[i][j] != '.':
                lb.append([g[i][j]])
                g[i][j] = '.'

    for b in lb:
        if not '#' in b:
            C += 1
            continue
        if '$' in b:
            T += 1


    # print(lb)

    return C, T




if __name__ == "__main__":
    M, N, P = [int(n) for n in input().split()]

    grid = [list(input()) for _ in range(M)]

    for _ in range(P):
        x, y = [int(i) for i in input().split()]

        if grid[x][y] == "#":
            grid[x][y] = '$'

    c, t = analyse(grid, M, N)

    print("%d %d" %(c, t))

