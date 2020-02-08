# 
# Enoncé
# 
# Dans ce challenge, l'objectif est de déterminer le mot le plus long dans un dictionnaire.
# 
# Format des données
# 
# Entrée
# Ligne 1 : un entier N compris entre 10 et 1000 représentant le nombre de mots contenus dans le dictionnaire.
# Ligne 2 à N+1 : une chaîne comprenant entre 1 et 750 caractères non accentués en minuscules représentant un mot du dictionnaire.
# 
# Sortie
# Un entier indiquant le nombre de caractère composant le mot le plus long du dictionnaire.

lines = open("/home/admin/Documents/trainBattleDev/ex1/input2.txt","r").read()

lines_temp = lines.split()
print(lines_temp)

line_length = [len(line) for line in lines_temp[1:-1]]
print(max(line_length))