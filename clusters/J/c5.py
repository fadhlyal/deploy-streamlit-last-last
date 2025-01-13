def problemJ(N):
    count = 0
    iterator = 0
    length = len(N)
    
    while iterator < length :
        if(N[iterator] == 'a' or N[iterator] == 'i' or N[iterator] == 'u' or N[iterator] == 'e' or N[iterator] == 'o') :
            count += 1
        
        iterator += 1
    
    return count