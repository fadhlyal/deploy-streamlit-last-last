def problemJ(N):
    count = 0
    
    for word in N :
        if(word == 'a' or word == 'i' or word == 'u' or word == 'e' or word == 'o') :
            count += 1
    
    return count