# coding=utf-8
Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/minesweeper.pdf

Objectif

Le célèbre jeu du démineur (https://fr.wikipedia.org/wiki/D%C3%A9mineur_(jeu)) se joue sur un champ de mines représenté par une grille en 2 dimensions. Chaque case de la grille peut soit contenir une mine, soit être libre. Les cases ont toutes leur contenu masqué au début, et le but est de découvrir toutes les cases libres sans faire exploser les mines, c'est-à-dire sans cliquer sur les cases qui les dissimulent. (Si vous voulez jouer, c'est ici : http://demineur.hugames.fr/#level-3).

Lorsque le joueur clique sur une case pour la dévoiler, si elle est libre, un chiffre apparaît sur cette case, indiquant, parmi les cases avoisinantes (qui sont au nombre de 8 si la case ne se trouve pas au bord de la grille), combien contiennent des mines. En comparant les différentes informations récoltées, le joueur peut ainsi progresser dans le déminage du terrain. S'il se trompe et clique sur une mine, il a perdu.

Si lorsqu'il clique sur une case, toutes les cases voisines sont libres, un zéro devrait apparaître, pour rendre l'affichage moins lourd, le jeu affiche une case blanche. Le joueur peut savoir qu'il peut cliquer sans risque sur toutes les cases voisines : le jeu lui économise cet effort en déclenchant un clic automatique sur les cases voisines, qui sont alors dévoilées, ce qui peut éventuellement déclencher d'autres clics automatiques, et ainsi de suite, jusqu'à ce que la zone vide soit entièrement délimitée par des cases dont le voisinage contient au moins une mine.

Dans l'exemple ci-dessous, le joueur a cliqué sur la case rouge et a dévoilé 40 cases :


Le but de ce challenge est de déterminer combien de cases vont être dévoilées par ce premier clic (en incluant la case du premier du clic).


Données

Entrée

Ligne 1 : un entier H compris entre 6 et 1000, représentant le nombre de lignes de la grille.
Ligne 2 : un entier L compris entre 6 et 1000, représentant le nombre de colonnes de la grille.
Lignes 3 à H+2 : une ligne de la grille représentée par une chaîne de L caractères. Les caractères de la ligne sont soit * (une mine), soit . (case vide), soit x (position du clic initial ; ce caractère apparaît exactement une fois dans la grille).

Sortie

Un entier, représentant le nombre de cases que le premier clic va dévoiler sur la grille (en incluant la case du premier clic).


#**************************************
#* Solution by Isograd
#**************************************
h = int(input())
l = int(input())
t = [input() for i in range(h)]

ii = -1
jj = -1

for i in range(h):
    for j in range(l):
        if t[i][j] == 'x':
            ii = i
            jj = j

visited = [[False for j in range(l)] for i in range(h)]
count = 0

def dfs(i,j):
    global count
    nbhood = [(i+x, j+y) for x in [-1,0,1] for y in [-1,0,1]
              if 0 <= i+x and i+x < h and 0 <= j+y and j+y < l]
    count += 1
    visited[i][j] = True
    if all(t[x][y] != '*' for (x,y) in nbhood):
        for (x,y) in nbhood:
            if not visited[x][y]:
                dfs(x,y)

dfs(ii,jj)
print(count)

