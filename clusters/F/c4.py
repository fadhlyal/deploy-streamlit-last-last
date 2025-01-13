def problemF(N):
    result = ""
    
    if(N < 0) :
        result = "Negative"
    elif(N > 0) :
        result = "Zero"
    else :
        result = "Positive"
    return result