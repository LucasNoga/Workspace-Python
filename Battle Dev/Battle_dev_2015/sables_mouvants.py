Énoncé



L'objet de ce challenge est de déterminer la profondeur maximale des zones de sable mouvant d'un désert. Le désert est un rectangle composé de cases de terre ferme ou de sable mouvant. La profondeur d'une case de sable mouvant est le nombre minimal de déplacements horizontaux et/ou verticaux à effectuer pour accéder à une case de terre ferme.







Dans l'exemple ci-dessus les cases de terre ferme sont représentées par des . et les chiffres représentent la profondeur des cases de sable mouvant. La case en rouge a une profondeur de 2 car il faut faire au moins deux déplacements horizontaux et/ou verticaux (par exemple, un vers le haut et un vers la gauche, ou bien 2 vers la gauche) pour atteindre la terre ferme.



La terre ferme n'est pas nécessairement connexe, il peut y avoir des îles de terre ferme au milieu des sables mouvants. Par ailleurs, sur tout le contour de la carte rectangulaire, il n'y a que de la terre ferme.



Format des données



Entrée

Ligne 1 : deux entiers H et L compris entre 3 et 40 séparés par un espace, indiquant respectivement la hauteur et la largeur de la carte.

Lignes 2 à H+1 : les lignes de la carte représentées par des chaînes de L caractères. Les caractères de la ligne sont soit . (terre ferme) soit # (sable mouvant).



Sortie

Un entier représentant la profondeur maximale des zones de sable mouvant du désert.


#*******
#* Solution by ISOGRAD
#*****/
N, M = map(int, input().split())
desert = []
for _ in range(N):
    desert.append(list(input()))
dist = [[0] * M for _ in range(N)]
for i in range(1, N - 1):
    for j in range(1, M - 1):
        dist[i][j] = min(dist[i - 1][j], dist[i][j - 1]) + 1 if desert[i][j] == '#' else 0
for i in range(N - 2, 0, -1):
    for j in range(M - 2, 0, -1):
        if desert[i][j] == '#' and min(dist[i + 1][j], dist[i][j + 1]) + 1 < dist[i][j]:
            dist[i][j] = min(dist[i + 1][j], dist[i][j + 1]) + 1
deepest = 0
for line in dist:
    deepest = max(deepest, max(line))
print(deepest)
