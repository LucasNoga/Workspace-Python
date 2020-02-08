# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/hydropons.pdf

Objectif

Il y a fort longtemps, dans une galaxie lointaine, très lointaine… Vous habitez une planète désertique à deux soleils, et êtes le modeste exploitant d’une ferme hydroponique. Votre exploitation est représentée par une grille carrée sur laquelle sont disposés des évaporateurs d’humidité. Chaque évaporateur d’humidité irrigue et rend ainsi cultivables les 8 cases qui lui sont adjacentes (on ne peut rien cultiver sur une case contenant un évaporateur d’humidité).

Le but de ce challenge est de déterminer le nombre de cases cultivables de votre exploitation.


Données

Entrée

Ligne 1 : un entier N compris entre 3 et 50 représentant la taille de votre ferme (une grille carrée de dimension N x N)
Lignes 2 à N+1 : les lignes de la carte représentées par des chaînes de N caractères. Les caractères de la ligne sont soit X (un évaporateur) soit . (une case vide).

Sortie

Un entier représentant le nombre de cases cultivables de votre ferme.



#***************************************************************
#*
#*
#* SOLUTION BY kosii
#*
#*
#******************************************************************
#*******
#* Read input from STDIN
#* Use echo or print to output your result, use the /n constant at the end of each result line.
#* Use:
#*      local_print (variable );
#* to display simple variables in a dedicated area.
#* ***/
import sys

N = int(sys.stdin.readline())

gr = set()

for i in range(N):
    l = sys.stdin.readline()[:-1]
    for j in range(N):
        if l[j] == 'X':
            gr.add((i, j))

res = set()
for g in gr:
    x, y = g
    for (a, b) in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        if 0 <= x+a < N and 0 <= y+b < N and (x+a, y+b) not in gr:
            res.add((x+a, y+b))
print(len(res))

