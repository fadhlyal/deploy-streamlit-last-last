def problemF(N):
    return ["negative", "zero", "positive"][(N > 0) - (N < 0) + 1]