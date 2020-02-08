n=int(input("Saisir n:"))
i=1
x=int(input("Saisir x:"))
Min=x
Max=x
while i<n:
    x=int(input("Saisir x:"))
    if x > Max:
          Max=x
    if (x<Min):
          Min=x
    i=i+1
print("Le Max est:",Max)
print("Le Min est:",Min)

        
