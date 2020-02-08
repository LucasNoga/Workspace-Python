H=int(input("Saisir H:"))
i=1
import sys
while i<=H:
    j=1
    while j<=i:
        sys.stdout.write("*")
        j=j+1
    print("")
    i=i+1
i=H-1
while i>=1:
    j=1
    while j<=i:
        sys.stdout.write("*")
        j=j+1
    print ("")
    i=i-1
    

