Z=0
Cpt=0

while Z<=10:
    Y=0
    while 10*Z+5*Y<=100:
        X=0
        while 10*Z+5*Y+2*X<=100:
            if 10*Z+5*Y+2*X==100:
                print(X,Y,Z)
                Cpt=Cpt+1
            X=X+5
        Y=Y+2
    Z=Z+1
print("Il éxiste",Cpt,"manières de faire un franc")
