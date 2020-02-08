class Humain:

    humains_crees = 0#attribut classe

    def __init__(self, v_prenom, v_age):
        print("\nCreation d'un humain")
        self.prenom = v_prenom
        self.age = v_age
        Humain.humains_crees += 1

print("Lancement du programme")

print("\nHumains existant {}".format(Humain.humains_crees))

h1 = Humain("Jojo", 34)
print("Prenom de h1 : {}".format(h1.prenom))
print("Age de h1 : {}".format(h1.age))

print("\nHumains existant {}".format(Humain.humains_crees))


h2 = Humain("Marek", 18)
print("Prenom de h2 : {}".format(h2.prenom))
print("Age de h2 : {}".format(h2.age))

print("\nHumains existant {}".format(Humain.humains_crees))
