def problemE(game) :
    final_cond = (game[0] > 0) and ((game[2] == 1 and game[1] >= 1000) or (game[2] == 2 and game[1] >= 3000) or (game[1] >= 7000))

    game_over = not(final_cond)

    return game_over