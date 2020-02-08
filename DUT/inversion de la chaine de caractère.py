def tableau (c):
    if len(c)==0:
        return""
    else:
        return(tableau(c[1:])+c[0])
c=input("saisir la chaine")
print(tableau (c))
