T=[15,4,5,9,36,25,17,28,65,14,25,96,58,47,35]
print (T)
i=0
x=0
j=0
while j< 14:
    i=0
    while i<14:
        while T[i]>T[i+1]:
            x=T[i+1]
            T[i+1]=T[i]
            T[i]=x

        i+=1
    j+=1
print(T)
            
            
    
                 
