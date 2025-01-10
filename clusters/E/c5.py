def problemE(N):
    a,b = N[0], N[1]
    c = a+b
    if c +(a*b) == 111:
        return 'yes'
    else:
        return 'no'