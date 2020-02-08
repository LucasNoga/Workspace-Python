from random import *
Ordinateur = "IA"
Bob = "Bob"



def nombre_choisi_par_ordinateur():
    return randrange(100)

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

print ("l'IA choisi un nombre")
nb = nombre_choisi_par_ordinateur()

print(Bob + " A toi de deviner le nombre")
deviner_nombre(nb)