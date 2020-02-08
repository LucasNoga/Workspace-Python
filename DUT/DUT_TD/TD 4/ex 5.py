# code pour savoir si le mot saisi est un palindrome ou pas
chaine = input("saisir un mot : ")
n = x = y = j = f = 0
T = []
for j in range(len(chaine)):
    T.append(chaine[j])
    n += 1

while (n/2) > x and f == 0:
    if T[x] == T[n-x-1]:
        y += 1
        x += 1
    else:
        f = 1
if f == 0:
    print(chaine, "est un palindrome")
else:
    print(chaine, "n'est pas palindrome")
