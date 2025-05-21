def problemE(game) :
    alive = game[0] > 0
    cond1 = game[2] == 1 and game[1] >= 1000
    cond2 = game[2] == 2 and game[1] >= 3000
    cond3 = game[1] >= 7000

    final_cond = alive and (cond1 or cond2 or cond3)

    return not(final_cond)