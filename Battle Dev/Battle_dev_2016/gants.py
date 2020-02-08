Objectif

L'hiver approche, c'est le moment de préparer vos vacances au ski. L'objectif de ce challenge est de déterminer combien de paires de gants vous pouvez constituer à partir des gants que vous trouvez dans votre tiroir.

Une paire de gants est constituée de deux gants de même couleur.

Format des données

Entrée
Ligne 1 : un entier N compris entre 1 et 1000 représentant le nombre de gants.
Ligne 2 à N + 1 : une chaîne comprenant entre 1 et 7 caractères en minuscules représentant la couleur d'un gant.

Sortie
Un entier représentant le nombre de paires que vous pouvez constituer. Pour constituer une paire, il faut deux gants de la même couleur.

from collections import Counter

N = int(input())
colors = []
for _ in range(N):
    s = input()
    colors.append(s)
nb_pairs = 0
for k, v in Counter(colors).items():
    if v > 1:
        nb_pairs += v // 2
print(nb_pairs)