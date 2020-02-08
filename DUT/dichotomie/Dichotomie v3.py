i=1
C=1
T=[]
N=int(input("Taille du tableau :"))

for i in range(N):
        T.append(i)
        print(T)


D=0
F=N-1
M=(D+F)//2

X=int(input("X:"))

while T[M] != X and D <= F:
    if T[M]> X:
        F=M-1
    else:
        D = M+1
    M=(D+F)//2



if T[M]!=X:
    print("Non trouvé")
else:
    print("X en est en position ",M)

