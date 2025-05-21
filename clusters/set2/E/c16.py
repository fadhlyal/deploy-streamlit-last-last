def problemE(game) :
    health = game[0]
    score = game[1]
    level = game[2]

    return not((health > 0) and ((level == 1 and score >= 1000) or (level == 2 and score >= 3000) or (score >= 7000)))