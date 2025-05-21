def problemB(number) :
    a = number[0]
    b = number[1]
    c = number[2]

    selisih1 = b-a
    selisih2 = c-b

    if(selisih1 != 1 and selisih2 != 1) :
        return "tidak"

    return "ya"