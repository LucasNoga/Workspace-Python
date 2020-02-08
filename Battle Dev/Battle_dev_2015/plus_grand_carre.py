Énoncé



Dans ce challenge vous devez déterminer la longueur du côté du plus grand carré contenant uniquement des symboles #.



Si la carte contient :



alors le résultat est 2, atteint par le carré 2 × 2 de # en rouge sur la carte.



Format des données



Entrée

Ligne 1 : deux entiers H et L compris entre 1 et 300 séparés par un espace, indiquant respectivement la hauteur et la largeur de la carte.

Lignes 2 à H+1 : les lignes de la carte représentées par des chaînes de L caractères. Les caractères de la ligne sont soit . soit #.



Sortie

Un entier représentant la longueur du côté du plus grand carré entièrement rempli de # de la carte.

# *****
# Solution de Cygin
# **/

import sys

H, L = map(int, input().split())

G = []
for i in range(H):
    G.append(input())

DP = [[0] * L for i in range(H)]
res = 0
for i in range(H - 1, -1, -1):
    for j in range(L - 1, -1, -1):
        if G[i][j] == '.':
            pass
        elif i == H - 1 or j == L - 1:
            DP[i][j] = 1
        else:
            DP[i][j] = min(DP[i + 1][j + 1], min(DP[i + 1][j], DP[i][j + 1])) + 1
        res = max(res, DP[i][j])
print(res)

