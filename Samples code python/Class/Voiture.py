class Voiture:
    roues = 4
    moteur = 1

    def __init__(self):
        self.nom = "A déterminer"

    def allumer(self):
        print("La voiture démarre")
        print(__name__)


class VoitureSport(Voiture):
    def __init__(self):
        self.nom = "Ferrari"

    def allumer(self):
        Voiture.allumer(self)
        print("La voiture de sport démarre")


print(__file__)
ma_voiture_sport = VoitureSport()
ma_voiture = Voiture()
print(ma_voiture)

print(ma_voiture.__dict__)

ma_voiture_sport = VoitureSport()
print(ma_voiture_sport.nom)
