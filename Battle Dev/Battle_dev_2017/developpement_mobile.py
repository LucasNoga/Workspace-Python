# coding=utf-8

Enoncé

Les applications mobiles tiennent un rôle de plus en plus important dans un monde où le smartphone est devenu un objet incontournable.
Une entreprise décide d’animer son réseau de consommateurs en créant un jeu concours autour d’une application mobile à télécharger. Les meilleurs joueurs seront récompensés avec des bons de réduction.

Le but du jeu est de dessiner une croix sur une partie de l'écran. La croix doit suivre les deux diagonales d'un carré de dimension D. D est un nombre impair supérieur ou égal à 3, tiré au hasard. Pour représenter le dessin, on va considérer une matrice où chaque point de la croix est représenté par un # et où les autres points sont représentés par des –.

Exemple

Si D vaut 5, la croix aura l'allure suivante:
#---#
-#-#-
--#--
-#-#-
#---#
Si D vaut 7, la croix aura l'allure suivante:
#-----#
-#---#-
--#-#--
---#---
--#-#--
-#---#-
#-----#


Format des données

Entrée
Ligne 1 : un entier impair D correspondant à la taille du carré contenant a croix

Sortie
N lignes de N caractères représentant la croix. Chaque caractère pouvant être un # ou un -.
Si vous rencontrez des problèmes avec les sauts de ligne dans votre sortie, vous pouvez aussi renvoyer une ligne unique comprenant toutes les lignes du dessin, en séparant chaque ligne du dessin par un espace. Par exemple si N=3 votre sortie serait :
#-# -#- #-#


# ***************************************************************
# *
# *
# * SOLUTION BY Kibo
# *
# *
# ******************************************************************
# *******
# * Read input from STDIN
# * Use echo or print to output your result, use the /n constant at the end of each result line.
# * Use:
# *      local_print (variable );
# * to display simple variables in a dedicated area.
# * ***/
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
d = int(lines[0])
lines = lines[1:]


def croix(etage, taille, upOrDown):
    chaine = ""
    if (etage >= 0):

        for _ in range(etage):
            chaine += "-"

        chaine += "#"

        # milieu
        for _ in range(taille - 2 - etage * 2):
            chaine += "-"

        if etage != taille // 2:
            chaine += "#"

        for _ in range(etage):
            chaine += "-"

        print(chaine)
        if etage == taille // 2 or upOrDown == "down":
            croix(etage - 1, taille, "down")
        else:
            croix(etage + 1, taille, "up")


croix(0, d, "up")

local_print("d =" + str(d));

