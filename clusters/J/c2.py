def problemJ(words):
    count = 0
    iterator = 0
    
    while iterator < len(words) :
        if(words[iterator] == 'a' or words[iterator] == 'i' or words[iterator] == 'u' or words[iterator] == 'e' or words[iterator] == 'o') :
            count += 1
        
        iterator += 1
    
    return count