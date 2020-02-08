Énoncé



Alors que votre grand-mère vous prépare votre tarte préférée, il se produit une coupure de courant. Vous explosez de joie, enfin un événement inédit pour perturber cette routine interminable. À la centrale, on vous explique qu'un troupeau de brebis a décroché tous les câbles. Vous remarquez que les câbles étaient de toute façon branchés n'importe comment (certains se croisaient) et aimeriez faire quelque chose de propre. Mais il faut agir dans l'urgence, donc pour commencer, il faut rebrancher un maximum de câbles, en conservant leurs extrémités, mais sans créer de croisement.



Voici une illustration vue de haut. À gauche, la disposition des câbles avant décrochage. À droite, un maximum de câbles rebranchés ne se croisant pas.







Pour valider ce problème, il vous faudra ruser : il n'est pas question de tester toutes les possibilités. Le nombre d'opérations à effectuer doit être au maximum de l'ordre du million.



Format des données



Entrée

Ligne 1 : un entier N représentant le nombre de câbles au total. N est compris entre 1 et 1000.

Lignes 2 à N + 1 : deux entiers D et F séparés par un espace et compris entre 1 et 1 000 000. D et F représentent la position sur le bornier de départ et la position sur le bornier d'arrivée d'un câble donné.



Il n'y aura pas deux câbles identiques dans les données.



Sortie

Un entier représentant le nombre maximal de câbles que vous pouvez rebrancher sans qu'il se croisent. Il peut y avoir plusieurs câbles sur la même entrée ou sur la même sortie.



Explication de la solution



Une fois les câbles triés par première extrémité croissante, le problème se résout à la recherche d'une plus longue suite croissante (pour la 2ème extrémité).

On pouvait le résoudre en O(n^2) par programmation dynamique, en maintenant pour chaque câble i le plus grand nombre de câbles j ≤ i sans croisement *si on accepte de prendre le i-ième*.

Appelons longest_until(i) cette valeur. Alors longest_until(i) peut se déduire des longest_until(j) pour j < i : il suffit de parcourir toutes les câbles j < i, et si le câble j ne croise pas le câble i, alors longest_until(j) + 1 est un candidat pour la valeur longest_until(i).

À la fin, il faut renvoyer le plus grand élément du tableau longest_until (et non son dernier élément, car le dernier câble ne sera pas forcément choisi dans l'ensemble optimal).

# ********Solution by Cygin **************
N = int(input())
C = []
for i in range(N):
    d, f = map(int, input().split())
C.append((d, f))
C.sort()

Fs = set()
for (d, f) in C:
    Fs.add(f)
Fs = list(Fs)
Fs.sort()

Ftonew = dict()
for i in range(len(Fs)):
    Ftonew[Fs[i]] = i

for i in range(N):
    C[i] = Ftonew[C[i][1]]

MF = len(Fs)

P = [[0] * (MF + 1) for i in range(N + 1)]

for i in range(N - 1, -1, -1):
    for
f in range(MF - 1, -1, -1):
P[i][f] = max(P[i + 1][f], P[i][f + 1])
if C[i] >= f:
    P[i][f] = max(P[i][f], 1 + P[i + 1][C[i]])
print(P[0][0])



