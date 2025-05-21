def problemB(number) :
    a = number[0]
    b = number[1]
    c = number[2]

    konsekutif = "tidak"

    if(b-a == 1 and c-b == 1) :
        konsekutif = "ya"

    return konsekutif