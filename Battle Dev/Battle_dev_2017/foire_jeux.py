# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/gamefair3.pdf

Objectif

Vous êtes très fier de votre collection de jeux rétro, mais il vous en manque quelques uns. Heureusement, vous avez rencontré d'autres collectionneurs avec qui échanger pour obtenir les jeux en rupture de stock que vous n'avez jamais eu dans le cadre d'un troc mutuellement bénéfique.

Vous commencez par recenser les jeux que chacun détient, ainsi que ceux que chacun souhaiterait avoir. Puis vous commencez par tenter de regrouper les gens par paires pour qu'ils s'échangent mutuellement leurs jeux, mais vous vous rendez compte qu'il est possible de faire encore mieux. En effet, si Alice aimerait bien avoir un jeu appartenant à Carole et possède un jeu qui intéresse Bob, tandis que Carole voudrait obtenir l'un des jeux de Bob, alors ils peuvent s'arranger comme suit : Alice donne à Bob, Bob donne à Carole, et Carole donne à Alice ; en fin de compte, chacun a reçu le jeu qui l'intéressait en échange de son don, et tous les trois sont contents ! On peut bien sûr imaginer des boucles plus longues.

On va ici essayer d'organiser un échange où chaque personne qui participe donne exactement un jeu et en reçoit exactement un. Un tel échange se compose donc d'une ou plusieurs boucles, de sorte que chaque participant soit impliqué dans au maximum une boucle.

Il est possible que certaines personnes qui auraient voulu participer à l'échange ne puissent pas le faire finalement, auquel cas elles ne donnent rien et ne reçoivent rien. Imaginons par exemple que seule Alice détienne le jeu qui intéresse Ève : dans ce cas, Alice étant déjà impliquée dans une boucle avec Bob et Carole, elle ne voudra pas donner à Ève en plus. Cette dernière sera donc exclue de cette boucle.

Cependant, la situation ainsi décrite n'est pas forcément optimale : peut-être aurait-il mieux fallu qu'Alice échange avec Ève et Bob avec Carole, en formant ainsi deux boucles de 2 personnes au lieu d'une boucle de 3 personnes. Encore faut-il pour cela qu'Ève ait quelque chose à donner à Alice et que Carole détienne un jeu qui intéresse à Bob…

Votre but est de concevoir un algorithme qui indique à chacun à qui il devrait faire don d'un jeu, afin de réaliser un échange où le nombre de personnes mises à l'écart est le plus petit possible.

Données

Entrée
Ligne 1 : un entier N compris entre 2 et 500 représentant le nombre de personnes souhaitant participer à l'échange.
Ligne 2 : un entier M, compris entre 2 et 1600 indiquant le nombre de lignes qui suivent.
Lignes 3 à M+2 : deux entiers i et j, séparés par une espace, signifiant que la personne d'identifiant i peut donner à celle d'identifiant j un jeu qui l'intéresse. i et j sont compris entre 1 et N. Il est possible que certaines personnes n'apparaissent pas dans ces lignes ni en donneur, ni en receveur. Inversement, une personne peut avoir des jeux à donner à plusieurs personnes et peut aussi être intéressée par un ou plusieurs jeux.

Sortie
Une ligne de N entiers, séparés par des espaces, décrivant un échange optimal : le i-ème nombre vaut :- 0 si la personne i est exclue de l'échange ;
- sinon, un entier j compris entre 1 et N, qui indique à qui la personne i donnera un jeu.
L'objectif est donc de minimiser le nombre de zéros tout en formant une ou plusieurs boucles ou chacun reçoit et donne un jeu. Une personne ne peut appartenir qu'à au plus une boucle. Dans le cas où aucun échange n'est possible, vous devez exclure tout le monde de l'échange, donc renvoyer une ligne ne contenant que des zéros.




TOLERANCE = 1e-6

def kuhn_munkres(G):
    assert len(G) == len(G[0])
    n = len(G)
    U = V = range(n)
    mu = [None] * n
    mv = [None] * n
    lu = [max(row) for row in G]
    lv = [0] * n
    for root in U:
        n = len(G)
        au = [False] * n
        au[root] = True
        Av = [None] * n
        marge = [(lu[root] + lv[v] - G[root][v], root) for v in V]
        while True:
            ((delta, u), v) = min((marge[v], v) for v in V if Av[v] == None)
            assert au[u]
            if delta > TOLERANCE:
                for u0 in U:
                    if au[u0]:
                        lu[u0] -= delta
                for v0 in V:
                    if Av[v0] is not None:
                        lv[v0] += delta
                    else:
                        (val, arg) = marge[v0]
                        marge[v0] = (val - delta, arg)
            assert abs(lu[u] + lv[v] - G[u][v]) <= TOLERANCE
            Av[v] = u
            if mv[v] is None:
                break
            u1 = mv[v]
            assert not au[u1]
            au[u1] = True
            for v1 in V:
                if Av[v1] is None:
                    alt = (lu[u1] + lv[v1] - G[u1][v1], u1)
                    if marge[v1] > alt:
                        marge[v1] = alt
        while v is not None:
            u = Av[v]
            prec = mu[u]
            mv[v] = u
            mu[u] = v
            v = prec
    return (mu,  sum(lu) + sum(lv))


n = int(input())
m = int(input())
G = [[float('-inf')] * n for i in range(n)]
for i in range(n):
    G[i][i] = 0
for i in range(m):
    u, v = map(int, input().split())
    G[u - 1][v - 1] = 1
mu, val = kuhn_munkres(G)

for i in range(len(mu)):
    if mu[i] == i:
        mu[i] = 0
    else:
        mu[i] += 1

print(' '.join(str(u) for u in mu))

