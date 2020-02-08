Énoncé



Deux pavés droits* A et B sont dits en collision si une partie de l'un est recouverte par l'autre (c'est-à-dire, s'ils ont un volume en commun). Dans ce challenge, vous allez devoir déterminer si deux pavés droits dont les faces sont parallèles aux axes du référentiel sont en collision.



(*)En géométrie, un pavé droit, ou parallélépipède rectangle, est une figure solide délimitée par six faces rectangulaires. Tous les angles sont des angles droits et les faces opposées du cuboïde sont égales.



Format des données



Entrée

Ligne 1 : six nombres entiers compris entre -10 et 10 séparés par des espaces représentant les coordonnées du pavé droit A : x1a y1a z1a x2a y2a z2a où (x1a, y1a, z1a) désigne le coin de A le plus proche de l'origine et (x2a, y2a, z2a) son coin le plus éloigné de l'origine.

Ligne 2 : les coordonnées du pavé B en utilisant la même représentation que celle utilisée pour le pavé A.



Sortie

La chaine de caractères Collision si les pavés A et B entrent en collision, la chaîne de caractères Pas de collision sinon.


/*Solution de chaign_c*/
import sys

input = list()

x1a ,y1a ,z1a ,x2a ,y2a ,z2a = [ int(i) for i in sys.stdin.readline().rstrip('\n').strip().split(' ') ]
x1b ,y1b ,z1b ,x2b ,y2b ,z2b = [ int(i) for i in sys.stdin.readline().rstrip('\n').strip().split(' ') ]

#x1a, x2a = min(x1a, x2a), max(x1a, x2a)
#y1a, y2a = min(y1a, y2a), max(y1a, y2a)
#z1a, z2a = min(z1a, z2a), max(z1a, z2a)


if (x2a > x1b and x1a < x2b and
        y2a > y1b and y1a < y2b and
        z2a > z1b and z1a < z2b):
    print("Collision")
else:
    print("Pas de collision")

