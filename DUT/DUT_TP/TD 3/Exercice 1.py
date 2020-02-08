Y=-5
Max=Y
Min=Y
T=-5
while T<=5:
    Y=2*T**3-T**2-37*T+36
    T=T+0.25
    if Y<=Min:
        Min=Y
    if Y>=Max:
        Max=Y
print (Min)
print (Max)
