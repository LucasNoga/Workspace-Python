z = i = 0
while z <= 10:
    y = 0
    while 10*z + 5*y <= 100:
        x = 0
        while 10*z + 5*y + x*2 <= 100:
            if 10*z + 5*y + 2*x == 100:
                print(z, y, x)
                i += 1
            x += 5
        y += 2
    z += 1

