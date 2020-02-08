# Énoncé
#
# Près de chez vous, il y a un terrain vague avec des poteaux de différentes hauteurs. Pourquoi ne pas tirer parti de cet emplacement publicitaire ?
#
# Les poteaux sont équidistants et séparés les uns des autres par une distance d'un mètre. Vous pouvez accrocher une banderole entre deux poteaux s'il n'y a pas de poteau strictement plus grand entre eux. On vous donne la hauteur de tous les poteaux, vous devez déterminer la longueur totale de banderole que vous pouvez y accrocher.
#
#
#
# Dans cet exemple la longueur totale est de 17 (9+6+1+1).
#
# Notez qu'il est tout à fait possible d'avoir 3 poteaux à la même hauteur, auquel cas si par exemple ils se trouvent aux positions 1 3 et 7 et qu'il n'y a pas de poteau plus haut qu'eux entre 1 et 7, on pourra accrocher une banderole de 1 à 3 et une banderole de 3 à 7 soit une longueur totale de 3 - 1 + 7 - 3 = 6.
#
# Votre code devra avoir une complexité N log N
#
# Format des données
#
# Entrée
# Ligne 1 : un entier N compris entre 1 et 100000 indiquant le nombre de poteaux de l'entrée.
# Lignes 2 à N+1 : un entier compris entre 1 et 100000 représentant la hauteur d'un poteau.
#
# Sortie
# Un entier représentant la longueur totale de banderole que vous pourrez accrocher sur les poteaux en considérant que la distance entre deux poteaux consécutifs est de 1 mètre.

try:
    lines = open("./input_bandexroles.txt", "r").read()
except FileNotFoundError:
    print("Oops!  That was no valid number.  Try again...")
    exit(1)

data = lines.split()
data = list(map(int, data))
print(data)


def readForward(list, i):
    index = i
    listInterne = []
    while index < len(list) - 1:
        index += 1
        listInterne.append(list[index])
    return listInterne


dicoVal = {}
for value in data:
    if value in dicoVal:
        dicoVal[value] += 1
    else:
        dicoVal[value] = 1
print(dicoVal)


def positionPoteaux(dicoVal, value):
    positions = [i for i, j in enumerate(data) if j == value]
    return positions


def hauteurPoteaux(data, poteauAtValue):
    count = 0
    bool_hauteur = 0
    for i, pos in enumerate(poteauAtValue[:-1]):
        hauteurs = data[poteauAtValue[i] + 1:poteauAtValue[i + 1]]
        for hauteur in hauteurs:
            if hauteur > data[poteauAtValue[i]]:
                bool_hauteur += 1
        if bool_hauteur == 0:
            count += poteauAtValue[i + 1] - poteauAtValue[i]
    return count


countFinal = 0
for value in set(data):
    if dicoVal[value] > 1:
        poteauAtValue = positionPoteaux(dicoVal, value)
        hauteurAtValue = hauteurPoteaux(data, poteauAtValue)
        countFinal += hauteurAtValue

print("La longueur totale de la banderole est de ", countFinal, " metres")
