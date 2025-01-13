def problemH(numb):
    result = ""
    
    for i in range(numb) :
        number = (i+1)**2
        result += str(number) + " "
    
    return result