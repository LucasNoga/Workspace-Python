a = float(input("saisir a : "))
b = float(input("saisir b : "))
c = float(input("saisir c : "))
Delta = d = b**2-4*a*c

if Delta < 0:
    print("pas de solution dans R")
if Delta > 0:
        x1 = (-b-d)/(2*a)
        x2 = (-b+d)/(2*a)
        print("les solutions sont", x1, x2)
if Delta == 0:
    x0 = (-b)/(2*a)
    print("les solutions sont", x0)
