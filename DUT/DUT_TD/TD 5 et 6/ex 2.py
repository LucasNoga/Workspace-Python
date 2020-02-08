# code qui permet d'inverser les element d'un tableau génerés aléatoirement

from random import randint
T=[]
a=0
i=0
k=0
n=int(input("quelle taille voulez vous pour votre tableau  T ? "))
j=n-1
for a in range (n):
    T.append(randint(100,1000))
print("T =", T)
print("----------")
while i < j:
    k = T[i]
    T[i] = T[j]
    T[j] = k
    i += 1
    j -= 1
print("T =", T)
