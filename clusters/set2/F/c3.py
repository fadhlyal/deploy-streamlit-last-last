def problemF(number) :
    bilangan = number[0]

    count = 0
    i = 1

    while(i <= bilangan) :
        if(bilangan%i == 0) :
            count += 1
        i += 1

    return count