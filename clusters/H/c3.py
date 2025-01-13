def problemH(number):
    result = ""
    iterator = 1
    
    while iterator <= number :
        result += str(iterator**2) + " "
        iterator += 1
    
    return result