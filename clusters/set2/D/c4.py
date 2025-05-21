def problemD(number) :
    bilangan = number[0]

    s_bilangan = str(bilangan)

    if(int(s_bilangan[0])%2 == 1 and int(s_bilangan[-1])%2 == 0) :
        hasil = 1
    else :
        hasil = 0

    return hasil