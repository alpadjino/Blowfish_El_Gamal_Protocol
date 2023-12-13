def ferma_iteration_count(chance: float):
    if chance < 0.5 or chance >= 1:
        raise ValueError("Chance could not be >0.5 or >=1")
    iterations = 1

    while 1 - pow(1/2, iterations) < chance:
        iterations += 1
    return iterations