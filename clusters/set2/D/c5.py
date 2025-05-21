def problemD(number) :
    bilangan = number[0]

    s_bilangan = str(bilangan)

    digit_awal = int(s_bilangan[0])
    digit_akhir = int(s_bilangan[-1])

    if(digit_awal%2 == 1 and digit_akhir%2 == 0) :
        return 1
    else :
        return 0