taille = int(input("Entrez la taille du tableau : "))
T = []
i = 0
while i < taille:
    val = int(input("Entrez une valeur : "))
    T.append(val)
    i += 1
print(T)
cpt = taille-1
for xbase in T:
    xmobile = 1
    for xmobile in T:
        print(T)
        if T[xbase] == T[xmobile]:
            T.remove(T[xmobile])
            taille -= 1
            cpt += 1
print(T)

