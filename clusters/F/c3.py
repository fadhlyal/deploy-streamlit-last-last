def problemF(N):
    result = ""
    
    if(N < 0) :
        result = "negative"
    elif(N > 0) :
        result = "zero"
    else :
        result = "positive"
    return result