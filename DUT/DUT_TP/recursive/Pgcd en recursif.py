def pgcd(a,b):
    while b>0:
      R=a%b
      a,b=b,R
    return a;
a=int(input("saisir a "));
b=int(input ("saisir b"));
print (pgcd(a,b));
