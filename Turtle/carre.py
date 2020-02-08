from turtle import*
def carre(longueur):
    forward(longueur)
    left(90)
    forward(longueur)
    left(90)
    forward(longueur)
    left(90)
    forward(longueur)
    left(90)

def figure(nb_carre, cote, angle):
    for i in range(nb_carre):
        carre(cote)
        left(angle)

up()
goto(-100, 100)
down()
figure(12, 50, 30)
up()
goto(0, -100)
down()
figure(24, 80, 15)
up()
goto(100, 100)
down()
figure(24, 10)
done()