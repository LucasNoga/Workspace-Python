#Fonction simplifiée
#n=int(input(Saisir un entier),10)
#print(bin(n))


n=int(input('Saisir un entier'))
Q=n
T=list()
while Q>0:
    T.append(Q%2)
    Q=int(Q/2)

T.reverse()
print(T)
