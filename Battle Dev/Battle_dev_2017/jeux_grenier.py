# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/gamesoftheattic5.pdf

Objectif

Vous êtes l'heureux détenteur d'une vaste et diverse collection de jeux vidéo, et vous vous demandez à quel point elle couvre une longue période de l'histoire du jeu vidéo. Pour cela, vous cherchez à déterminer quelle est la plus longue durée qui s'est écoulée entre les sorties de deux jeux dans votre collection.

Données

Entrée
Ligne 1 : un entier N représentant le nombre de jeux dans votre collection.
Lignes 2 à N+1 : un entier indiquant l'année de parution d'un de vos jeux.

Sortie
Un entier, représentant la plus grande différence (en nombre d'années) entre deux années de parution.











# Solution by Isograd
import sys

lines = []
for line in sys.stdin:
	lines.append(line.rstrip('\n'))

lines.pop(0)
dates = list(map(int, lines))
print(max(dates) - min(dates))


