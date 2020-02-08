Énoncé



L'objectif de ce challenge est de sortir d'un labyrinthe en cassant le moins de murs possible. En effet, vous disposez d'un marteau qui vous permet de casser des murs. Une fois un mur cassé, il disparaît définitivement du labyrinthe et la case devient libre.

Le labyrinthe est un rectangle de dimensions N x M. La case en haut à gauche a pour coordonnées (0,0). Vous entrez par la case (1, 0) et vous cherchez à sortir par la case (N - 1, M - 2). Chaque case du labyrinthe peut être libre ou contenir un obstacle.



Format des données



Entrée

Ligne 1 : deux entiers N et M inférieurs à 100 et séparés par un espace correspondant respectivement à la hauteur et la largeur du labyrinthe.

Lignes 2 à N+1 : des chaines de M caractères représentant le labyrinthe. Les cases libres sont représentées par un point "." tandis que les obstacles sont représentés par un croisillon "#".

Le contour du labyrinthe est exclusivement composé d'obstacles, hormis à l'entrée (1, 0) et la sortie (N - 1, M - 2). L'entrée et la sortie contiennent des ".", ils ont été remplacés par E et S sur l'illustration ci-dessus pour clarifier l'exemple.



Sortie

Un entier représentant le nombre minimal d'obstacles à démolir pour sortir du labyrinthe. S'il n'y a pas d'obstacle à démolir, affichez 0.

#Solution d'Arthur
N, M = [int(i) for i in input().rstrip('\n').split(' ')]
lab = []
seen = []
for _ in range(N):
    lab.append([c == '.' for c in list(input().rstrip('\n'))])
    seen.append([-1]*M)

import queue

q = queue.PriorityQueue()
q.put((0, 1, 0))
while not q.empty():
    obs, x, y = q.get()
    if x == N-1 and y == M-2:
        print(obs)
        break
    else:
        for k, l in ((x+1, y), (x-1,y),(x,y+1),(x,y-1)):
            if 0 <= k < N and 0 <= l < M:
                d = 0 if lab[k][l] else 1
                if seen[k][l] == -1 or seen[k][l] > obs + d:
                    seen[k][l] = obs+d
                    q.put((obs + d,k,l))

