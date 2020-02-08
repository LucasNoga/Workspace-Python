def power(x,n):
  c=n
  power=x
        
  if n==0:
        power=1
  if n==1:
        power=x
  if n>1:
       i=1
       while i<n:
              power=power*x
              i+=1
       return power;

x=float(input("saisir l'exposé"));
n=int(input("saisir l'exposant"));
print ( power(x,n));

       
