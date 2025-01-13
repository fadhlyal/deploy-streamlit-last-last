def problemI(N):
    result = 1
    iterator = 0
    
    while iterator < N :
        number = iterator + 1
        result *= number
        iterator += 1
    
    return result