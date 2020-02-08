from random import randint

T = []
a = 0
i = 0
k = 0
j = int(input("taille jusqu'à m ? "))
n = int(input("Taille du tableau complet ? "))
m = j

while m >= n:
    m = int(input("taille jusqu'à m ? "))
    n = int(input("Taille du tableau complet ? "))

for x in range(n):
    T.append(randint(100, 1000))
print(T)
print("----------")
i = 0
while i < n:
    k = T[i]
    T[i] = T[j]
    T[j] = k
    i = i+1
    n = n-1
    j = j+1
    
print(T)
