def problemI(N):
    result = 1
    iterator = 1
    
    while iterator <= N :
        number = iterator
        result *= number
        iterator += 1
    
    return result