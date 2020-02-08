Énoncé

Aujourd'hui, la réussite des entreprises repose sur un moteur de recherche efficace, robuste aux fautes de frappe et d'orthographe, ces dernières devenant d'ailleurs progressivement des réformes de la langue française.

On vous donne une liste de mots d'un dictionnaire, ainsi qu'une liste de mots tapés par un internaute distrait. Pour chaque mot tapé par l'utilisateur, vous devez afficher le mot le plus proche du dictionnaire. Le mot le plus proche du dictionnaire représente le mot de plus faible coût que l'on puisse obtenir à partir du mot de l'internaute qui soit dans le dictionnaire. Pour déterminer le coût total, chacune des petites opérations suivantes représente un certain coût :- L'ajout d'une lettre (arbre -> arbore) a un coût de 2 ;
- La suppression d'une lettre (globe -> lobe) a un coût de 2 ;
- Le remplacement d'une lettre par une autre (barbe -> barre) a un coût de 3 ;
- Et enfin, l'échange de deux lettres consécutives (orbe -> robe) a un coût de 3.En cas d'égalité, affichez le plus petit mot dans l'ordre alphabétique.

Par exemple, le coût pour passer du mot algorithme à rythme est 11 (4 suppressions, 1 remplacement) et celui pour passer d'algorithme à logarithme est 7 (1 suppression, 1 ajout, 1 remplacement : algo -> lgo -> logo -> loga).

Format des données

Entrée
Ligne 1 : un entier D compris entre 1 et 200 indiquant le nombre de mots du dictionnaire.
Lignes 2 à D+1 : un mot du dictionnaire, tout en minuscules et sans caractère accentué, ne dépassant pas 15 lettres.
Ligne D+2 : un entier N compris entre 1 et 200 indiquant le nombre de mots tapés par l'internaute.
Lignes D+3 à D+N+2 : un mot tapé par l'internaute, tout en minuscules et sans caractère accentué, ne dépassant pas 15 lettres.

Sortie
Pour chaque mot tapé par l'internaute, vous devez afficher le mot le plus proche du dictionnaire. En cas d'égalité, affichez le premier mot dans l'ordre alphabétique.



def damerau_levenshtein_distance(a, b):
    n = len(a)
    m = len(b)
    dist = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if min(i, j) == 0:
                dist[i][j] = max(i, j) * 2
            elif i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                dist[i][j] = min(dist[i - 1][j] + 2,
                                 dist[i][j - 1] + 2,
                                 dist[i - 1][j - 1] + 3 * (a[i - 1] != b[j - 1]),
                                 dist[i - 2][j - 2] + 3)
            else:
                dist[i][j] = min(dist[i - 1][j] + 2,
                                 dist[i][j - 1] + 2,
                                 dist[i - 1][j - 1] + 3 * (a[i - 1] != b[j - 1]))
    return dist[n][m]

N = int(input())
words = []
for _ in range(N):
    words.append(input())
M = int(input())
for _ in range(M):
    contestants = []
    s = input()
    for i in range(N):
        contestants.append((damerau_levenshtein_distance(s, words[i]), words[i]))
    _, answer = min(contestants)
    print(answer)