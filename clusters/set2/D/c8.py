def problemD(number) :
    bilangan = number[0]

    if((bilangan//1000)%2 == 1 and (bilangan%10)%2 == 0) :
        return 1
    else :
        return 0