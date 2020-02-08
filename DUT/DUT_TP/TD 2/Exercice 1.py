A=int(input("Saisir A:"))
B=int(input("Saisir B:"))
C=int(input("Saisir C:"))
X=0
Y=0
Delta=B**2-4*A*C

if Delta>=0:
    X=(-B-pow(Delta,1/2))/(2*A)
    Y=(-B+pow(Delta,1/2))/(2*A)
print(X)
print(Y)

if Delta==0:
    Z=-B/2*A
if Delta<0:
    print("Erreur dans la matrice")
