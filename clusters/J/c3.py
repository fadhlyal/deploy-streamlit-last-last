def problemJ(N):
    count = 0
    
    for i in range(len(N)) :
        if(N[i] == 'a' or N[i] == 'i' or N[i] == 'u' or N[i] == 'e' or N[i] == 'o') :
            count += 1
    
    return count