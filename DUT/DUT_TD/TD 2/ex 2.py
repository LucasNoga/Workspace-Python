m = 0
while m <= 9:
    n = 0
    while pow(m, 2)+2 * pow(n, 2)+2 < 100:
        print([m, n])
        n += 1
    m += 1
