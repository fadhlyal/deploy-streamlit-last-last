def problemD(N):
    x,y = N[0], N[1]
    if x==0 or y==0:
        return 'no'
    elif y==39:
        return 'yes'
    elif y*2==x:
        return 'yes'
    else:
        return 'no'