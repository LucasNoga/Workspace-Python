n=int(input("saisir une valeur: "))
def fibo(n):
    if n==0:
        return 1;
    elif n==1:
        return 1;
    else:
        return fibo(n-1) + fibo(n-2);
print (fibo(n))


    
    
