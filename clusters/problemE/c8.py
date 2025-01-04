def problemE(N):
    N = str(N)
    M = len(N)
    if M == 1:
        return "satuan"
    elif M == 2:
        return "puluhan"
    elif M == 3:
        return "ratusan"
    elif M == 4:
        return "ribuan"
    elif M == 5:
        return "puluhribuan"