n=int(input("Saisir n:"))
S1=1
i=2
while i<=n:
    if i%2==0:
        S1=S1-1/i
        i=i+1
    else:
        S1=S1+1/i
        i=i+1
print("S1=",S1)

