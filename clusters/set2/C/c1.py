def problemC(dice) :
    d1 = dice[0]
    d2 = dice[1]
    d3 = dice[2]

    hasil = d1%2 == 0 and d2%2 == 0 and d3%2 == 0

    return hasil