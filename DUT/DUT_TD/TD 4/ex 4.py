N = int(input("Nombre de valeur a saisir : "))
T = []
i = 0
while i < N:
    a = int(input("entrez une valeur : "))
    T.append(a)
    i += 1
print(T)
print(i)
i = c = 0
b = int(input("entrez maintenant la valeur a cherché : "))
while i < N:
    if T[i] == b:
        c += 1
    i += 1
print(c)
