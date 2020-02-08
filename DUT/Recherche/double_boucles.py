

# matrice 1
print()
print()
for i in range(10):
    for j in range(10):
        j+=i
        if j>=10:
            j-=10
        print(j," ",end='')
    print()


print()
print()
print('############################################')
print('############################################')
print('############################################')
print()
print()


# matrice 2
print()
print()
for i in range(10):
    print(i)
    z = i+1
    for j in range(10):
        while z>0:
            j=0
            z-=1
        print(j," ",end='')
    print()

print()
print()