from random import *
def genere_liste(n):
    return [randrange(100) for i in range(n)]

print(genere_liste(10))