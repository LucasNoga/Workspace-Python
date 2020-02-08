from math import*
import random
from sys import *
import sys
import time

def coordo(M):
 coord=0
 while coord<8:
         cordx=random.randint(1,19)
         cordy=random.randint(1,49)
         print(cordx, cordy)
         M[cordx][cordy]='X'
         coord+=1
         T.append([cordx,cordy])
         


def matrice(aff):
  aff[0]=['-' for i in range (50)]
  aff[19]=['-' for i in range(50)]


  for i in range (20):
        aff[i][0]='|'
        aff[i][49]='|'

  for i in range(20):
          for j in range (50):
                  sys.stdout.write(aff[i][j])
          print()
def norme(T):
    for b in range(8):
        print("-------")
        for d in range(8):
                if (b==d):
                    print((T[b][0])**2+(T[d][1])**2)
                else:
                    print(sqrt(( T[b][0]-T[d][0])**2+(T[b][1]-T[d][1])**2))

                

T=[]
M=[[' ' for i in range (51)]for j in range(21)]
coordo(M)
matrice(M)
norme(T)

        
         
        
         
         
