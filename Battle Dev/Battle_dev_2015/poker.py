Enoncé



Dans ce challenge, l'objectif est de déterminer la somme qu'a un joueur à la fin d'une partie de poker. Le joueur dispose d'une somme initiale. À chaque tour, le joueur mise un montant X. Puis il gagne un montant Y pouvant être positif ou nul. Le bilan pour chaque tour est donc -X+Y.



Votre code doit renvoyer le montant restant au joueur à la fin de la partie.



Format des données



Entrée

Ligne 1 : un entier entre 1 000 et 10 000 représentant la somme dont le joueur dispose au départ.

Ligne 2 : un entier N entre 10 et 45 représentant le nombre de tours joués.

Lignes 3 à N+2 : deux entiers positifs ou nuls séparés par un espace représentant X et Y tels que définis dans l'énoncé.



La série des mises et des montants remportés fait que le joueur ne sera jamais ruiné et aura toujours un montant restant positif ou nul.





Sortie

Un entier indiquant la somme restante au joueur à la fin de la partie.

#*******
#solution by MDF-31
#*********
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

initial = int(lines[0])
nbretour = int(lines[1])
for i in range(2, 2 + nbretour):
   X = int(lines[i].split(' ')[0])
   Y = int(lines[i].split(' ')[1])
   initial = initial - X + Y

print(initial)