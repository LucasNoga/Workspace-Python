from turtle import*
def rectangle(longueur, largeur):
    forward(longueur)
    left(90)
    forward(largeur)
    left(90)
    forward(longueur)
    left(90)
    forward(largeur)
    left(90)

def figure():
    for i in range(200):
        rectangle(80, 20)
        left(5)

figure()
done()
