# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/pacman2.pdf

Objectif

Vous êtes lâché dans un manoir hanté labyrinthique, habité par des fantômes qui veulent votre mort et la damnation éternelle de votre âme. Seul répit possible : atteindre la Pastille du Pouvoir, cachée quelque part dans la maison, qui vous permettra de lever la malédiction.

Le GPS de votre smartphone vous a permis de localiser la Pastille (ne demandez pas comment, il y a des choses que l'humanité n'est pas encore prête à apprendre). Vous connaissez également les plans du manoir et l'emplacement actuel des fantômes. Pouvez-vous atteindre la Pastille du Pouvoir sans croiser de fantôme ?

Le manoir est représenté par un quadrillage où vous comme les fantômes pouvez, à chaque unité de temps, choisir de vous déplacer sur l'une des 4 cases adjacentes, si celle-ci n'est pas un mur, ou bien de rester sur place. De plus, le sortilège ayant altéré la topologie des lieux, lorsque vous vous trouvez sur une case au bord gauche, votre case voisine à gauche est en fait la case à l'extrémité droite de la même ligne ; réciproquement, en vous déplaçant à droite depuis le bord droit, vous arrivez sur le bord gauche. De même, les cases du bord haut sont voisines des cases du bord bas. Les fantômes subissent le même sortilège.

Vous cherchez à atteindre la Pastille en vous déplaçant de sorte à vous assurer de ne pas être intercepté par l'un des fantômes et vous ne connaissez pas à l'avance leurs déplacements. Une case est mortelle à partir d'un instant t, si un fantôme peut s'y trouver à l'instant t. Il vous est demandé de planifier votre trajet de sorte à ne jamais passer par une case qui est mortelle au moment où vous y êtes. Par exemple, une case qu'un fantôme ne peut atteindre qu'avec au moins 2 déplacements est mortelle à partir de l'instant 2, si votre trajet vous y fait passer à l'instant 3 (où à n'importe quel instant supérieur ou égal à 2), vous êtes intercepté.

On vous demande de déterminer le temps minimum nécessaire pour atteindre la Pastille sans être intercepté. Précision : la case de la Pastille ne doit pas être mortelle au moment où vous y parvenez ; autrement dit, si un fantôme peut y arriver avant ou en même temps que vous, vous avez perdu.

Données

Entrée
Ligne 1 : un entier N compris entre 1 et 1000, indiquant la hauteur de la carte, qui est égale à sa largeur.
Lignes 2 à N+1 : les lignes de la carte représentées par des chaînes de N caractères. Les caractères de la ligne sont soit # (mur), soit . (case traversable), soit une lettre majuscule repérant une position distinguée : C pour la position de votre personnage, M pour celle d'un fantôme et O pour l'emplacement de la Pastille.

En particulier, il y aura toujours une seule occurrence de C et de O dans une carte, mais autant de M qu'il n'y a de fantômes différents (il peut n'y en avoir aucun).

Sortie
Un entier, indiquant le nombre minimal d'unités de temps nécessaire pour atteindre la Pastille en empruntant un chemin qui ne passe par aucune case qui est mortelle au moment où vous y passez. Si c'est impossible, renvoyez 0.




from collections import namedtuple
from heapq import heappop, heappush

Point = namedtuple("Point", ['x', 'y'])
BFSPoint = namedtuple("BFSPoint", ["n", 'point'])


def read_input():
    n = int(input())
    return n, [input() for i in range(n)]


def find_pastille(laby):
    for x in range(len(laby)):
        for y in range(len(laby[x])):
            if laby[x][y] == 'O':
                return Point(x, y)


def solve(size, laby):
    pastille_pos = find_pastille(laby)
    heap = [BFSPoint(0, pastille_pos)]
    seen = set(pastille_pos)
    dist_c = float('+inf')
    while heap:
        n, point = heappop(heap)
        if n > dist_c:
            break
        if laby[point.x][point.y] == 'M':
            return 0
        if laby[point.x][point.y] == 'C':
            dist_c = n
        for xd, yd in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            point2 = Point((point.x + xd) % size, (point.y + yd) % size)
            if point2 not in seen and laby[point2.x][point2.y] != '#':
                heappush(heap, BFSPoint(n + 1, point2))
                seen.add(point2)
    if dist_c == float('+inf'):
        return 0
    return dist_c


print(solve(*read_input()))

