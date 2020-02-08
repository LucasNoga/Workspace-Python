n=float(input("entrez un nombre"))
while n<10 or n>20:
    if n<10:
        print("plus grand")
    elif n>20:
        print("plus petit")
    n=float(input("entrez un nombre"))
print ("c'est bon")