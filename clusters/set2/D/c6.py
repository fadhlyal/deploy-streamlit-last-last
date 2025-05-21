def problemD(number) :
    bilangan = number[0]

    s_bilangan = str(bilangan)

    if(int(s_bilangan[0])%2 == 1 and int(s_bilangan[-1])%2 == 0) :
        return 1
    else :
        return 0