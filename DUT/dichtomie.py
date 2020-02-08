
import random
t=[]
n=int(input("Saisir nombre d'entier: "))
for i in range(n):
    t.append(random.randint(0,200))
t.sort()
print(t)
X=int(input("Saisir le nombre a chercher "))
d=0
f=n-1
m=(d+f)//2
while d<=f and t[m] != X:
    if t[m]>X:
        f=m-1
    if t[m]<X:
        d=m+1
    m=(d+f)//2
if d>=f:
    print(X, " n'est pas dans ", t)
else:
    print(X, " est à la ", m+1, "eme position dans ", t) 
        
 
