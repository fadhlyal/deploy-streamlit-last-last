def problemH(numb):
    result = ""
    iterator = 1
    
    while iterator <= numb :
        number = iterator**2
        result += str(number) + " "
        iterator += 1
    
    return result