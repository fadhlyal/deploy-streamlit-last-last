def problemE(N):
    a,b = N[0], N[1]
    sum=a+b+(a*b)
    if sum==111:
        return "YES"
    else:
        return "NO"