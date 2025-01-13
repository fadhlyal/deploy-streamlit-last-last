def problemG(N):
    result = ""

    if(N > 90) :
        result =  "A"
    elif(N > 70) :
        result = "B"
    elif(N >= 40) :
        result = "C"
    else:
        result = "F"

    return result