Alice = "Alice"
Bob = "bob"

def choisir_nombre():
    bon_nombre = False;
    while not bon_nombre:
        nb = int(input("Veuillez choisir un nombre entre 1 et 100 : "))
        if (nb<0 or nb>100):
            print("Veuillez choisir un nombre entre 1 et 100 : ")
        else:
            bon_nombre = True
    return nb

def deviner_nombre(nb):
    trouve = False
    while not trouve:
        nb2=int(input("Donne moi un nombre : "))
        if nb==nb2:
            trouve = True
        elif nb<nb2:
            print("plus petit")
        elif nb>nb2:
            print("plus grand")

    print("Felicitations le nombre a deviner est: " + str(nb))

print (Alice + " Choisi un nombre")
nb = choisir_nombre()

print(Bob + " A toi de deviner le nombre")
deviner_nombre(nb)


