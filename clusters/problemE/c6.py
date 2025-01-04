def problemE(masukan):
    konversi = str(masukan)
    patokan = 0
    for test in konversi:
        patokan = patokan + 1
    if patokan == 1:
        return "satuan"
    elif patokan == 2:
        return "puluhan"
    elif patokan == 3:
        return "ratusan"
    elif patokan == 4:
        return "ribuan"
    elif patokan == 5:
        return "puluhribuan"
    elif patokan == 6:
        return "ratusribuan"