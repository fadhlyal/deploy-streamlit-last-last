def problemD(number) :
    bilangan = number[0]

    digit_awal = bilangan//1000
    digit_akhir = bilangan%10

    if(digit_awal%2 == 1 and digit_akhir%2 == 0) :
        return 1
    else :
        return 0