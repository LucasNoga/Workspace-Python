a = float(input("entrez un nombre : "))
p = float(input("entrez une précision : "))
chiffre = a
while pow(chiffre, 2)-a >= pow(p, 2):
    an = (1/2) * (chiffre+a / chiffre)
print(chiffre)
