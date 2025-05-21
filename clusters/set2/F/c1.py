def problemF(number) :
    bilangan = number[0]

    hitung = 0

    for i in range(1, bilangan+1) :
        if(bilangan%i == 0) :
            hitung += 1

    return hitung