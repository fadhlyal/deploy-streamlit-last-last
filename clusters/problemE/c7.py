def problemE(x):
    i = 0
    while x != 0:
        x //= 10
        i = i+1
    if i==1:
        return "satuan"
    if i==2:
        return "puluhan"
    if i==3:
        return "ratusan"
    if i==4:
        return "ribuan"
    if i==5:
        return "puluhribuan"