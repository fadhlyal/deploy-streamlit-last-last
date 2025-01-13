def problemH(numb):
    result = ""
    
    for i in range(1, numb+1) :
        number = i**2
        result += str(number) + " "
    
    return result