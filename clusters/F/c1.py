def problemF(N):
    return ["Negative", "Zero", "Positive"][(N > 0) - (N < 0) + 1]