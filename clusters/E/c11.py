def problemE(N):
    a,b = N[0], N[1]
    c=a+b+(a*b)
    if c==111:
        return "yes"
    else:
        return "no"