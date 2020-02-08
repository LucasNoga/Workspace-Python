# coding: utf-8
import os
from random import randrange
from math import ceil

roulette = []
global mise
argent = 1000
global numero


# debut de la partie
def debutDepartie():
    debutPartie = "Bienvenue à la roulette vous devez miser une somme sur un " \
                  "numero entre 1 et 49\nla mise est comprise entre 1$ et 1000$\n" \
                  "Vous disposer de " + str(argent) + "$"
    print(debutPartie)


# l'utilisateur choisi une mise
def miser():
    mise = input("Quelle mise voulez-vous faire ?\nMise : ")
    print("Vous avez misé " + str(mise) + "$")
    return mise


# l'utilisateur choisi un numero
def choisirNumero():
    numero = input("Quelle numero voulez-vous choisir ?\nNumero : ")
    print("Vous avez choisie le numero " + str(numero))
    return numero


# initialisation de la roulette
def initialisationRoulette():
    i = 0
    while i < 50:
        roulette.append(i)
        i = i + 1


# Verifie si la mise saisie est un nombre
def miseCorrecte(mise):
    mise = int(mise)
    if mise > 0 and mise < 1000:
        return True
    else:
        return False


# Verifie si le nombre est compris entre 0 et 49
def nombreChoisieCorrecte(nombre):
    nombre = int(nombre)
    if nombre >= 0 and nombre < 50:
        return True
    else:
        return False


# genere un nombre aleatoire est fait tourner la roulette
def tournerRoulette(mise, numero, argent):
    if argent <= 0:
        print("vous etes ruiné vous ne pouvez plus joué au revoir")
    else:
        print("\nlancement de la roulette")
        numeroRoulette = randrange(50)
        print("la roulette s'est arrete sur le numero " + str(numeroRoulette))
        if numero == numeroRoulette:
            print("Félicitations ! Vous obtenez " + str(mise) * 3 + "$ !")
            argent += mise * 3
        elif numero % 2 == numeroRoulette % 2:
            mise = ceil(mise * 0.5)
            print("Vous avez misé sur la bonne couleur. Vous obtenez " + str(mise) + "$")
            argent += mise
        else:
            print("Désolé l'ami, c'est pas pour cette fois. Vous perdez votre mise.")
            argent -= mise

        print("Vous avez à présent " + str(argent) + "$")
        quitter = input("Souhaitez-vous quitter le casino (o/n) ? ")
        print(quitter)
        if quitter == "o" or quitter == "O":
            print("Vous quittez le casino avec vos gains.")
        else:
            tournerRoulette(mise, numero, argent)

        # lancement de la partie


def lancemenentDePartie():
    debutDepartie()
    mise = miser()
    numero = choisirNumero()
    # initialisationRoulette()

    if miseCorrecte(mise) and nombreChoisieCorrecte(numero):
        tournerRoulette(mise, numero, argent)
    else:
        print("Vous n'avez pas saisi de bonne valeur")
        print("relancement de la partie")
        lancementDePartie();


lancemenentDePartie()
# On met en pause le système (Windows)
os.system("pause")
