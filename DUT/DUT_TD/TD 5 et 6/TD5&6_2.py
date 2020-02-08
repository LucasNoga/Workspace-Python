from random import randint
T = []
a = i = k = 0
n = int(input("taille de T ? "))
j = n-1

for a in range(n):
    T.append(randint(100, 1000))
print(T)
print("----------")

while i < j:
    k = T[i]
    T[i] = T[j]
    T[j] = k
    i = i+1
    j = j-1
print(T)
