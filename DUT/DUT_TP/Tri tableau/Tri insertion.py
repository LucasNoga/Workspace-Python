T=[4,5,8,12,32,3,2]
n=6
i=0
j=1
while i<=n:
    x=T[i]
    j=i
    while j>0 and T[j-1]>x:
        T[j]=T[j-1]
        j=j-1
    T[j]=x
    i=i+1
print(T)
