def problemE(N):
    if 0 <= N < 10:
        return "satuan"
    elif 10 <= N < 100:
        return "puluhan"
    elif 100 <= N < 1000:
        return "ratusan"
    elif 1000 <= N < 10000:
        return "ribuan"
    elif 10000 <= N < 100000:
        return "puluhribuan"