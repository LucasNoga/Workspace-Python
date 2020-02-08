# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/thelongjump3.pdf

Objectif

Vous avez ressorti un vieux jeu de plateforme de votre enfance et vous vous trouvez face à une succession délicate de sauts à effectuer. Le niveau à compléter est pourtant très simple : il ne contient que de la terre, toujours à la même hauteur, et quelques fossés où tomber entraînerait la mort de votre personnage. Mais ces derniers peuvent être d'une grande largeur, et, ne vous souvenant plus de la portée maximale possible d'un saut, vous n'êtes même pas certain que le niveau soit faisable.


Tout ce que vous savez, c'est que cette portée maximale est un certain nombre entier P de cases, et que vos déplacements possibles consistent à avancer d'une case en marchant, ou d'un nombre entre 2 et P de cases en sautant. On vous donne les cases du niveau ; déterminez la valeur minimale de P pour être en mesure, en partant du début du niveau (tout à gauche), d'arriver à la fin (tout à droite).


Données

Entrée
Ligne 1 : un entier N compris entre 3 et 60 indiquant la largeur du niveau.
Ligne 2 : une chaîne de N caractères représentant les cases successives du niveau : - pour une case de terre, _ pour une case de vide.


Sortie
Un entier représentant la plus petite portée maximale (c'est à dire la plus petite valeur de P) à partir de laquelle le niveau est faisable. Si aucun saut n'est nécessaire, renvoyez 1.



N = int(input())
terrain = input()


def solve(terrain):
    best = 0
    tmp = 0
    for char in terrain:
        if char == '_':
            tmp += 1
            if tmp > best:
                best = tmp
        elif char == '-':
            tmp = 0
    return best + 1

print(solve(terrain))

