# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/rollercoaster.pdf

Objectif

Vous êtes l'organisateur d'une attraction "Montagnes Russes". C'est un train qui monte et qui descend sur des rails. Votre attraction est configurable, en effet, vous disposez d'une série de poteaux de hauteurs différentes que vous pouvez mettre dans l'ordre que vous souhaitez. Ensuite vous les reliez avec des rails.

Vous pouvez donc décider du style de votre attraction. Par exemple si vous mettez vos poteaux du plus grand au plus petit, vous créez une descente. Si vous les ordonnez du plus petit au plus grand, vous obtenez une montée. Votre client du jour est une équipe de développeurs Salesforce. Ils n'ont peur de rien, ils vous ont donc demandé une configuration "nombre maximal de bosses". Pour arriver à cela il y a deux solutions :- Soit le premier poteau est suivi par un plus petit, puis par un plus grand, puis par un plus petit et ainsi de suite.
- Soit le premier poteau est suivi par un plus grand, puis par un plus petit, puis par un plus grand et ainsi de suite.
Exemple : Supposons que vous ayez 4 poteaux de hauteur 10, 20, 30 et 40 mètres. Alors, les deux configurations ci-dessous produiraient "un maximum de bosses". Il existe d'ailleurs d'autres configurations permettant le même résultat.


Données

Entrée

Ligne 1 : un entier N compris entre 4 et 300, représentant le nombre de poteaux dont vous disposez.
Ligne 2 à N+1 : un entier compris entre 10 et 1000 représentant la hauteur d'un poteau. Il n'y a pas 2 poteaux de la même hauteur.

Sortie

Un série d'entiers séparés par des espaces représentant les hauteurs des poteaux ordonnés de telle façon à créer "un maximum de bosses".



N = int(input())
poles = [int(input()) for _ in range(N)]
poles.sort()
soluce = []
for i in range(N//2):
    soluce.append(poles[i])
    soluce.append(poles[len(poles)-i-1])
if N % 2:
    soluce.append(poles[N//2])
print(" ".join(map(str, soluce)))

