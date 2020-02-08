n=int(input("Saisir N:"))
i=3
var1=1
var2=1
while i<=n:
    V=var1+var2
    var1=var2
    var2=V
    i+=1
print(V)
