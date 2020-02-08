# coding=utf-8


Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/spacepizza.pdf

Objectif

Bienvenue en l’an 3000. Le futur ne vous appartient pas, vous êtes un livreur de pizza malchanceux. Afin de livrer des commandes de pizzas, vous empruntez le réseau de transport à air comprimé ionisé de la ville de New New York. Les stations de ce réseau sont des points de l’espace décrits par le triplet de coordonnées x, y, z.

Vous commencez votre course dans la pizzeria du professeur située dans la station avec le y le plus petit, communément appelée « le bout du tube ». Le professeur pizzaïolo vous donne la liste des stations où se trouve un client ayant commandé une pizza.

Les stations sont reliées par des tuyaux et - nous sommes dans le futur - il existe un tuyau direct entre chaque paire de stations. Ce moyen de locomotion a beau être extrêmement rapide, il présente l’inconvénient (pour des raisons évidentes de différences de pressions) de n’être qu’à sens unique : vous vous déplacez toujours d’une station i vers j avec un yᵢ < yⱼ.

Vous ne pouvez revenir sur vos pas qu’en arrivant en bout de course dans ce que les voyageurs appellent communément « l’autre bout du tube » (la station avec le y le plus grand), où vous pourrez actionner un levier mécanique permettant d’inverser le flux d’air : vous pouvez alors vous déplacer dans l'autre sens c'est à dire d’une station i vers une station j avec yᵢ > yⱼ.

Ainsi deux stations ne peuvent se trouver sur le même y, afin qu’il existe toujours une pression suffisante pour que l’on puisse se déplacer à travers les tuyaux.

Quelle est la distance minimum que vous aurez à parcourir pour passer dans toutes les stations et retourner à la pizzeria ? Pour flatter votre égo, vous arrondirez au plus grand entier inférieur ou égal. On rappelle que la distance entre deux points de coordonnées (xi,yi,zi) et (xj,yj,zj) est donnée par :


Indication : On attend un algorithme de complexité quadratique dans le pire des cas.


Données

Entrée

Ligne 1 : un entier N compris entre 5 et 1000, représentant le nombre de total de stations : la station de départ plus toutes les stations ayant commandé des pizzas.
Lignes 2 à N+1 : les coordonnées entières xᵢ, yᵢ, zᵢ de la station i séparées par une espace. Toutes les coordonnées sont comprises entre 0 et 1000. Les stations sont dans un ordre aléatoire, donc la station de départ n'est pas nécessairement sur la ligne 2.

Sortie

Un entier représentant la distance minimale nécessaire pour livrer toutes vos pizzas en partant de la pizzeria et en revenant à la pizzeria, arrondi par défaut (à l’entier inférieur).


#***************************************************************
#*
#*
#* SOLUTION BY Christophe_3
#*
#*
#******************************************************************
from math import sqrt
from heapq import *

def d(p,q) :
    x,y,z=p
    a,b,c=q
    return sqrt((x-a)**2+(y-b)**2+(z-c)**2)

N=int(input())
T=[tuple(map(int,input().split())) for _ in range(N)]

T.sort(key=lambda p:p[1])

local_print(T)

D=[[d(T[i],T[j]) for i in range(N)] for j in range(N)]

def glouton() :
    best={}
    stack=[(D[0][1],1,0,2)]
    best[(1,0)]=D[0][1]
    heapify(stack)
    while True :
        d,l,r,n=heappop(stack)
        if n==N :
            return int(d)
        if n==N-1 : heappush(stack,(d+D[l][N-1]+D[r][N-1],n,n,n+1))
        else :
            left=d+D[l][n],n,r,n+1
            if (n,r) not in best or best[(n,r)]>left[0] :
                best[(n,r)]=left[0]
                heappush(stack,left)
            right=d+D[r][n],l,n,n+1
            if (l,n) not in best or best[(l,n)]>right[0] :
                best[(l,n)]=right[0]
                heappush(stack,right)


print(glouton())

