a = float(input("saisir a"))
b = float(input("saisir b"))
c = float(input("saisir c"))
if a < b+c and b < a+c and c < a+b:
    print("abc est un triangle")
else:
    print("abc n'est pas un triangle")
