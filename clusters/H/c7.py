def problemH(number):
    result = ""
    iterator = 0
    
    while iterator < number :
        result += str((iterator+1)**2) + " "
        iterator += 1
    
    return result