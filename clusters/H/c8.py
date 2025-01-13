def problemH(numb):
    result = ""
    iterator = 0
    
    while iterator < numb :
        number = (iterator+1)**2
        result += str(number) + " "
        iterator += 1
    
    return result