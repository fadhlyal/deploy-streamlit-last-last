def problemB(number) :
    a = number[0]
    b = number[1]
    c = number[2]

    selisih1 = b-a
    selisih2 = c-b

    hasil = "tidak"

    if(selisih1 == 1 and selisih2 == 1) :
        hasil = "ya"

    return hasil