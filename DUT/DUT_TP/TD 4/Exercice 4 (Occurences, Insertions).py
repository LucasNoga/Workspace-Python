n=int(input('Saisir le nombre de cases du tableau: '))
i=0
T=list()
while i<n:
    x=int(input('Saisir une valeur: '))
    T.append(x)
    i=i+1
print(T)
T.append(0) #Permettra de décaler les valeurs

#Affiche un tableau avec n entiers

i=0
j=0

y=int(input('Saisir la valeur à compter: '))
while i<n:
    if T[i]==y:
        j=j+1
    i=i+1
print("Le nombre d'occurences est de: ",j)

#Compte les occurences


i=n-1
z=int(input("Saisir la valeur que l'on veut ajouter au tableau: "))
p=int(input('Saisir la case à laquelle on veut insérer la valeur: '))
while i>=p:
    T[i+1]=T[i]
    i=i-1
T[p]=z
print(T)

#Insert une valeur dans un tableau
