def problemE(a):
    a = str(a)
    if(len(a) == 1) :
        return "satuan"
    elif(len(a) == 2) :
        return "puluhan"
    elif(len(a) == 3) :
        return "ratusan"
    elif(len(a) == 4) :
        return "ribuan"
    else :
        return "puluhribuan"