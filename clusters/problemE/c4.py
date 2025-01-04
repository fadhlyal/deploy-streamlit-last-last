def problemE(x):
    x = str(x)
    if (len(x) == 1) :
        return "satuan\n"
    elif (len(x) == 2) :
        return "puluhan\n"
    elif (len(x) == 3) :
        return "ratusan\n"
    elif (len(x) == 4) :
        return "ribuan\n"
    elif (len(x) == 5) :
        return "puluhribuan\n"
    elif(len(x) == 6) :
        return "ratusribuan\n"