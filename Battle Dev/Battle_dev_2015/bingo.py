Énoncé



Le Bingo est un jeu de hasard à un ou plusieurs joueurs.

Chaque joueur dispose d'une grille avec 5 lignes et 5 colonnes. Chaque case de la grille contient un nombre entre 1 et 100, tous différents. À chaque tour, un orateur tire un nombre au hasard entre 1 et 100 et l'énonce à voix haute. Chaque joueur peut alors rayer le nombre s'il apparaît dans sa grille.



Le premier à avoir rayé tous les nombres d'une même ligne, colonne ou diagonale remporte la partie (à condition de crier « Bingo ! »).



Dans ce challenge vous devez déterminer si vous avez gagné lors d'une séance de Bingo et si oui, à quel instant.



Format des données



Entrée

Lignes 1 à 5 : chaque ligne contient 5 nombres entiers entre 1 et 100 séparés par des espaces représentant la i-ième ligne de votre grille.

Ligne 6 : le nombre de tirages N compris entre 1 et 100.

Lignes 7 à N+6 : un nombre entier compris entre 1 et 100 correspondant à un tirage de l'orateur.

Tous les nombres de votre grille sont différents et tous les tirages sont des nombres différents.



Sortie

La chaîne de caractères OK t où t désigne le numéro du tour où vous devez crier « Bingo ! », c'est-à-dire le premier tour pour lequel tous les nombres d'une même ligne, colonne ou diagonale ont été rayés. Si votre grille n'est pas gagnante, la chaîne de caractères NOK.


#Solution d'Arthur
import sys

pos = {}
seen = [[False for _ in range(5)] for __ in range(5)]

grid = set()
for i in range(5):
    l = input().rstrip('\n').split(' ')
    for j, p in enumerate(l):
        pos[p] = (i, j)
b = True
N = int(input().rstrip('\n'))
for i in range(N):
    k = input().rstrip('\n')
    if k not in pos:
        continue
    n, m = pos[k]
    seen[n][m] = True
    if all(seen[n][mm] for mm in range(5)) or all(seen[nn][m] for nn in range(5)) or (n == m and all(seen[nn][nn] for nn in range(5))) or (n == 4 - m and all(seen[nn][4-nn] for nn in range(5))):
        print('OK {}'.format(i+1))
        b = False
        break
if b:
    print('NOK')

