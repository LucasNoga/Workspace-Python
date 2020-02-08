n = int(input("Saisir le nombre de test que vous allez effectuer : "))
nb = int(input("entrez un nombre de reference : "))
i = 1
minimum = nb
maximum = nb
while i <= n:
    nb = int(input("entrez un nombre de test : "))
    if nb < minimum:
        minimum = nb
    if nb > maximum:
        maximum = nb
    i += 1
    print("la valeur max est %d et la valeur min est %d" % (maximum, minimum))
