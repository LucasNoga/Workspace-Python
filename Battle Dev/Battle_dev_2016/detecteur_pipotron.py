# Enoncé
#
# Le Pipotron est un générateur automatique de phrases qui permet de facilement meubler la conversation. Le principe est que la phrase est conçue en ajoutant plusieurs composants les un derrières les autres et en ajoutant un espace entre chaque composant. Chaque composant est tiré au hasard. Par exemple, dans un Pipotron générant des phrases à 3 composants, on a une liste de possibilités pour le 1er composant, une liste de possibilités pour le 2ème composant et une liste de possibilités pour le 3ème composant. On tire au hasard un élément de la première liste, un élément de la seconde, un élément de la 3ème, on les met bout à bout en les séparant par des espaces et on obtient une phrase pleine de sens.
#
# On peut trouver des exemples ici :- http://richard.geneva-link.ch/excusotron.html
# - http://www.lepipotron.com/
# - http://www.chateauloisel.com/humour/pipotron.htm
# L'objectif de ce challenge est de déterminer si une phrase est un Pipotron.
#
# Il n'y as pas de contrainte de complexité sur l'algorithme.
#
# Format des données
#
# Entrée
# Ligne 1 : un entier n compris entre 3 et 5 représentant le nombre de composants du Pipotron.
# Ligne 2 : n entiers séparés pas des espaces représentant le nombre de chaînes possibles pour chaque composant du Pipotron. On nommera ces entiers P1,P2...Pn. Et on appellera T la somme P1 + P2 +...+ Pn.
# Ligne 3 à T + 2 : Les chaines possibles pour chaque composant du Pipotron. Chaque chaîne contient entre 2 et 150 caractères non accentués et peut contenir des majuscules et des ponctuations. Les P1 premières chaînes correspondent au premier composant puis de P1+1 à P1 + P2, les chaînes du second et ainsi de suite.
# Ligne T + 3: un entier Q représentant le nombre de phrases à vérifier.
# Ligne T + 4 à T + 3 + Q : une phrase comprenant entre 1 et 750 caractères qui peut être ou non un Pipotron.
#
# Sortie
# Un entier V représentant le nombre de Pipotrons dans les phrases proposées.

lines = open("./input_pipotron.txt", "r").read()

data = [line.strip() for line in lines.splitlines()]

nbComp = int(data[0])

nbCombo = [int(x) for x in data[1].split()]

sumCombo = sum(nbCombo)

charComp = data[2:sumCombo + 2]

testPipo = data[sumCombo + 3:]

comp1 = charComp[0:nbCombo[0]]
comp2 = charComp[nbCombo[0]:(nbCombo[0] + nbCombo[1])]
comp3 = charComp[(nbCombo[0] + nbCombo[1]):]

count = 0

phrases = []
for elem1 in comp1:
    for elem2 in comp2:
        for elem3 in comp3:
            phrases.append(' '.join([elem1, elem2, elem3]))
            count += 1

print(count)

print(phrases)

count = 0
for pipo in testPipo:
    print(pipo)
    if pipo in phrases:
        count += 1

print(count)


