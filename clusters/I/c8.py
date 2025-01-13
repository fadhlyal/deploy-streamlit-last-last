def problemI(number):
    result = 1
    
    for i in range(1, number+1) :
        number = i
        result *= number
    
    return result