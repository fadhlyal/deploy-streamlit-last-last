def problemE(game) :
    health = game[0]
    score = game[1]
    level = game[2]

    alive = health > 0
    cond1 = level == 1 and score >= 1000
    cond2 = level == 2 and score >= 3000
    cond3 = score >= 7000

    game_over = not(alive and (cond1 or cond2 or cond3))

    return game_over