def problemF(number) :
    bilangan = number[0]

    count = 0
    i = 0

    while(i <= bilangan-1) :
        if(bilangan%(i+1) == 0) :
            count += 1
        i += 1

    return count