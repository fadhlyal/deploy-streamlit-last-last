def problemF(number) :
    bilangan = number[0]

    count = 0

    for i in range(0, bilangan) :
        if(bilangan%(i+1) == 0) :
            count += 1

    return count