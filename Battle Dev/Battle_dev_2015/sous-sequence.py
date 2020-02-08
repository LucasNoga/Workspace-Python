#Solution TOSA

# Une chaîne X est sous-séquence d'une chaîne Y si l'on retrouve toutes les lettres de X dans la chaîne Y dans le bon ordre.
# Par exemple:- aab est une sous-séquence de aacb.

# - aab n'est pas une sous-séquence de aba.

# Dans ce challenge, vous devez déterminer si une chaîne est une sous-séquence d'une autre chaîne.

# Format des données

# Entrée
# Ligne 1 : la chaîne de caractères X
# Ligne 2 : la chaîne de caractères Y
# La longueur de chaque chaîne ne dépasse pas 1000 caractères.

# Sortie
# La chaîne de caractères OK si X est une sous-séquence de Y.
# Sinon, la chaîne de caractères NOK n où n représente la longueur (éventuellement 0) du plus grand préfixe de X qui soit sous-séquence de Y. On entend par préfixe de longueur n, la sous-chaîne égale aux n premiers caractères de X.

x = input()
y = input()
i = 0
c = 0
while i < len(y) and c < len(x):
    if x[c] == y[i]:
        c += 1
    i += 1
print('OK' if c == len(x) else 'NOK %d' % c)