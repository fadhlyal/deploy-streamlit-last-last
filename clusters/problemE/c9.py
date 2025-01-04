def problemE(N):
    panjang_digit = len(str(N))
    if panjang_digit == 1:
        return "satuan"
    elif panjang_digit == 2:
        return "puluhan"
    elif panjang_digit == 3:
        return "ratusan"
    elif panjang_digit == 4:
        return "ribuan"
    elif panjang_digit == 5:
        return "puluhribuan"