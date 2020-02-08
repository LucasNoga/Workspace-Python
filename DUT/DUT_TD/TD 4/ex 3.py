def saisir_date():
    jour = int(input("saisir un jour (2 chiffres) : "))
    if jour > 30 or jour < 1:
        print("Jour non valide")
        exit()
    if jour < 10:
        jour = "0"+str(jour)

    mois = int(input("saisir un mois (2 chiffres) : "))
    if mois > 12 or mois < 1:
        print("Mois non valide")
        exit()
    if mois < 10:
        mois = "0"+str(mois)

    annee = int(input("saisir une année (4 chiffres) : "))
    if annee > 2017 or annee < 0:
        print("Annee non valide")
        exit()

    print("la date est le", str(jour) + "/" + str(mois) + "/" + str(annee))

saisir_date()