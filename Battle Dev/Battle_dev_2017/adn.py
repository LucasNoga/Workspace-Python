# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/DNA.pdf

Objectif

Vous avez pour mission d’évaluer le potentiel génétique des candidats d’un nouveau centre spatial. Pour cela, vous avez développé une méthode de séquençage de leur ADN. Le candidat est une espèce à 1 chromosome double brin. C’est-à-dire que son ADN peut être vu comme deux chaînes de caractères a et b composées exclusivement des lettres A, C, G et T. Par ailleurs ces deux chaînes sont complémentaires, elles sont donc de même longueur et vérifient :- a[i] = A ⇔ b[i] = T
- a[i] = T ⇔ b[i] = A
- a[i] = C ⇔ b[i] = G
- a[i] = G ⇔ b[i] = CLors du séquençage, les deux chaînes se cassent en plusieurs petits fragments qui sont mélangés entre eux. Votre méthode n’est pas si mauvaise que ça, vous savez que l’ordre des caractères dans un fragment n’a pas été inversé. Vous êtes cependant obligé écrire un programme pour recoller les morceaux dans un ordre plausible. Pour vous assurer que vous n’avez oublié aucun fragment, votre programme renverra les deux chaînes a et b en séparant les différents fragments par des espaces.

Indication : l’ADN d’un candidat n’est pas très complexe, il n’y aura jamais plus de 8 fragments, vous pourrez donc procéder par énumération exhaustive (force brute).

Exemple

Si vous avez les fragments suivants :
AT
G
CC
TAG

Une solution possible est alors :

Ce qui donne la sortie suivante (voir plus bas pour le format de sortie) :
TAG G#AT CC
On pourrait bien sûr permuter les brins 1 et 2 et la solution serait aussi correcte.

Données

Entrée

Ligne 1 : un entier N compris entre 2 et 8, indiquant le nombre de fragments d’ADN.
Lignes 2 à N+1 : une chaine comprenant entre 1 et 16 caractères, composée exclusivement des lettres A, T, C, et G représentant un fragment.

Sortie
Une chaîne de caractères représentant les 2 brins. Les 2 brins sont séparés par le caractère # et dans un brin donné les fragments utilisés sont séparés par des espaces.


#***************************************************************
#*
#*
#* SOLUTION BY Lowik
#*
#*
#******************************************************************
import sys
from collections import defaultdict
from collections import deque
import heapq
from itertools import permutations


def check(a, b):
    matches = set([("A", "T"), ("T", "A"), ("C", "G"), ("G", "C")])
    at = "".join(a)
    bt = "".join(b)
    for ag, bg in zip(at, bt):
        if (ag, bg) not in matches:
            return False
    return True


def solve(adns):
    for p in permutations(adns):
        la = 0
        ia = 0
        while True:
            la += len(p[ia])
            ia += 1
            if la == mid:
                if check(p[:ia], p[ia:]):
                    print(" ".join(p[:ia]) + "#" + " ".join(p[ia:]))
                    return
                break
            elif la > mid:
                break

            if ia >= len(p):
                break

n = int(input())

adns = []
total = 0
for i in range(n):
    line = input().strip()
    adns.append(line)
    total += len(line)

mid = total // 2

solve(adns)


