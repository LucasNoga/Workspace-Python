Énoncé

Vous avez réussi avec brio à connecter tous les ordinateurs de l'entreprise ! Mais vous vous rendez compte que l'unique ordinateur connecté à Internet est à la périphérie du réseau local, ce qui signifie que si la fibre optique lâche à son niveau, tous les autres ordinateurs du réseau local seront privés d'Internet. À la place, vous aimeriez bien connecter à Internet un autre ordinateur du réseau local, de façon à ce qu'en cas de coupure d'un unique câble du réseau local, un minimum d'ordinateurs soient privés d'Internet.

On vous donne la topologie du réseau local, garantissant que deux ordinateurs quelconques sont reliés entre eux par un unique chemin de fibre optique. On vous laisse choisir quel unique ordinateur vous allez connecter à Internet de façon à minimiser le nombre d'ordinateurs dont la connexion à Internet sera compromise au pire, en cas de coupure d'un unique câble du réseau local. On vous demande quel est ce nombre d'ordinateurs qui seront privés d'Internet, au pire.

Exemple

Dans la topologie ci-dessous tirée de l'exercice précédent, il vaut mieux connecter à Internet l'ordinateur n° 3. Ainsi, cela garantit qu'au pire, en l'occurrence en cas de coupure du câble reliant l'ordinateur n° 2 à l'ordinateur n° 3 (comme sur la figure), 3 ordinateurs seront privés d'Internet (ceux avec une croix dans l'écran). La réponse à renvoyer est donc : 3.

Pour résoudre cet exercice, un algorithme de complexité linéaire est attendu.



Format des données

Entrée
Ligne 1 : un entier N compris entre 1 et 100000 représentant le nombre d'ordinateurs du parc informatique. Chaque ordinateur est identifié de façon unique par un entier compris entre 0 et N - 1.
Lignes 2 à N : deux entiers u et v (compris entre 0 et N - 1) et séparés par un espace indiquant que les ordinateurs u et v sont directement reliés par de la fibre optique dans le réseau local.

Sortie
Un entier représentant le nombre d'ordinateurs au maximum qui seront privés d'Internet dans le pire cas de coupure d'un unique câble réseau. Votre but étant de choisir quel ordinateur connecter à Internet pour minimiser ce nombre.

# *************Solution by Clement ******************/
import sys

sys.setrecursionlimit(1000000000)
n = int(input())
g = [[] for _ in range(n)]
for i in range(n - 1):
    u, v = map(int, input().split())
g[u] += [v]
g[v] += [u]

prof = [0 for i in range(n)]


def find(a, b):
    v = 1
    for c in g[a]:
        if c != b:
            v += find(c, a)
    prof[a] = v
    return (v)


mini = 1000000000


def find2(a, b, w):
    global mini
    v = w
    for c in g[a]:
        if c != b:
            v = max(v, prof[c])
            find2(c, a, w + prof[a] - prof[c])
    mini = min(mini, v)


x = find(0, -1)
find2(0, -1, 0)
print(mini)