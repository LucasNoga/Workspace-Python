Enoncé

Dans ce challenge, l'objectif est de déterminer le stock d'affiches publicitaires restantes dans le service marketing de Peugeot. Au début du mois, le dépôt contient X affiches publicitaires. Chaque jour, les différents sites de vente Peugeot commandent Y affiches.

Votre code doit renvoyer le nombre d'affiches restantes à la fin d'un mois.

Le service marketing étant très prévoyant, nous vous assurons qu'il y aura toujours suffisamment d'affiches en stock pour satisfaire la demande.

Format des données

Entrée
Ligne 1 : un entier X entre 1000 et 10 000 représentant le nombre d'affiches publicitaires au début du mois.
Ligne 2 : un entier N entre 28 et 31 représentant le nombre de jours dans le mois.
Ligne 3 à N+2 : un entier Y entre 50 et 100 représentant le nombre total d'affiches publicitaires commandées un jour donné. Il y a une ligne pour chaque jour.

Sortie
Un entier indiquant le nombre d'affiches publicitaires restant à la fin du mois.


#*******
#* SOLUTION BY BertrandBordage
#* ***/

x = int(input())
n = int(input())
for i in range(n):
    x -= int(input())
print(x)