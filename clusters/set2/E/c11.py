def problemE(game) :
    game_over = not((game[0] > 0) and ((game[2] == 1 and game[1] >= 1000) or (game[2] == 2 and game[1] >= 3000) or (game[1] >= 7000)))

    return game_over