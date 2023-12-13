from Big_Prime_Digit_Generator import big_prime_digit_generator
from Enum_Class import Direction
from Pow_Operations import pow_operations
import random

def primitive_root(p):
    q = (p - 1) // 2
    g = 0
    res = 1
    while res == 1:
        g = random.randint(2, p - 1)  # получили случайного кандидата на первообразный корень
        res = pow_operations.pow_mod(g, q, p)
    return g

def keys_generator(method_name: Direction, bit_lenght: int):
    p = big_prime_digit_generator(method_name, 0.99999999, bit_lenght)
    g = primitive_root(p)
    x = random.randint(p // 2, p - 2)
    y = pow_operations.pow_mod(g, x, p)
    k = random.randint(p // 2, p - 2)

    return (p, g, y), x, k