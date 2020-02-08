def affichage_ascii():
    print("Voici la liste des caractères ascii")
    for i in range(150):
        print(i, " : ", chr(i))


def affichage_lettre():
    code = input("Saisissez le code dont vous voulez connaître le caractère : ")
    print(chr(int(code)))


def affichage_code():
    c = input("Saisissez le caractère dont vous voulez connaître le code : ")
    print(ord(c))

def main():
    quitter = True
    while quitter:
        choix = input("Que voulez vous faire\n0 - Quitter le programme,\n1 - Affichage de la liste des ascii,\n"
                      "2 - Recherchez un caractère avec son code ascii,\n3 - Recherchez le code d'un caractère\n"
                      "Votre choix : ")

        if choix == "0":
            quitter = False

        elif choix == "1":
            affichage_ascii()

        elif choix == "2":
            affichage_lettre()

        elif choix == "3":
            affichage_code()

        else:
            print("je n'ai pas compris votre demande")

main()
