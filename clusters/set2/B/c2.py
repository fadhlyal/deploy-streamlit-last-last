def problemB(number) :
    a = number[0]
    b = number[1]
    c = number[2]

    hasil = "ya"

    if(b-a != 1 and c-b != 1) :
        hasil = "tidak"

    return hasil