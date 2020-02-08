Énoncé

Les distributeurs de friandises doivent faire face à toutes les situations possibles (stock épuisé, plus de pièces) afin de ménager le service client de l'entreprise.

En l'occurrence, vous devez programmer l'algorithme de rendu de monnaie de la machine, en veillant à rendre un minimum de pièces tout en respectant le stock de pièces s'y trouvant actuellement (si c'est possible).

Format des données

Entrée
Ligne 1 : un entier M, représentant le montant à rendre en euros. M est compris entre 1 et 25000.
Ligne 2 : un entier T, le nombre de types de pièces se trouvant dans la machine. T est compris entre 1 et 10.



#********Solution by Isograd **************
total = int(input())
N = int(input())
system = []
for _ in range(N):
    nb, amount = map(int, input().split())
    for _ in range(nb):
        system.append(amount)
nb_coins = len(system)
min_coins = [[float('inf')] * (total + 1) for _ in range(nb_coins + 1)]
min_coins[0][0] = 0
for i in range(1, nb_coins + 1):
    for j in range(total + 1):
        if j == 0:
            min_coins[i][j] = 0
        else:
            best = min_coins[i - 1][j]
            if j >= system[i - 1]:
                best = min(best, 1 + min_coins[i - 1][j - system[i - 1]])
            min_coins[i][j] = best
if min_coins[nb_coins][total] == float('inf'):
    print('IMPOSSIBLE')
else:
    print(min_coins[nb_coins][total])