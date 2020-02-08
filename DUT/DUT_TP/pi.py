# coding: utf-8

# Programme python qui calcul pi

from random import *
from math import *


def getPi():
    pointsCercle = 0
    nbPoints = 10000000
    for i in range(nbPoints):
        x = random()
        y = random()
        if pow(x, 2) + pow(y, 2) <= 1:
            pointsCercle += 1
        pi2 = pointsCercle / nbPoints * 4
        print(pi2)
    pi = pointsCercle/nbPoints*4
    return pi

if __name__ == "__main__":
    print("Veuillez attendre quelques secondes")
    print("pi vaut : {}", getPi())
