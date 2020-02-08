A=int(input("Saisir A:"))
P=int(input("Saisir P:"))
an=A
while an**2-A>=P**2:
    an=1/2*(an+A/an)
    print (an)
