Énoncé



Un facteur d'un mot est une suite de caractères consécutifs qui en est extraite.

Par exemple, le mot FINITION est un facteur de DEFINITION, mais NT n'est pas un facteur de DEFINITION.



L'objet de ce challenge est de déterminer le plus long facteur commun à deux chaînes de caractères.



Format des données



Entrée

Ligne 1 : un entier N compris entre 3 et 50 représentant le nombre de paires de chaînes de caractères.

Ligne 2 à N+1 : deux chaînes séparées par un espace contenant chacune entre 1 et 500 caractères. Les caractères sont uniquement des lettres en majuscules sans accent. La première chaîne représentant le premier mot et la seconde chaîne représentant le second mot.



Sortie

N lignes correspondant aux N paires de chaînes de l'entrée. Chaque ligne doit contenir le plus long facteur de la paire de chaînes. S'il existe plusieurs facteurs de longueur maximale, il faut afficher le premier dans l'ordre alphabétique. S'il n'existe pas de facteur commun aux deux chaînes de caractères, la ligne devra contenir la chaîne AUCUN FACTEUR.

#*****
# Solution de IIIIIIIIIIIII
#**/

import sys
import os

inp = sys.stdin
out = sys.stdout

def main():
    run()

def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set

def run():
    #local_print("--- Running ---/")
    nbPaires = int(inp.readline())

    for n in range(nbPaires):
        a, b = inp.readline().split()
        c = sorted(lcs(a, b))

        if len(c) > 0:
            print(c[0])
        else:
            print("AUCUN FACTEUR")

main()