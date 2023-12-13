from Pow_Operations import pow_operations
from Template_Class import PrimeTestTemplate
from Miller_Rabin_Iteration_Count import miller_rabin_it_count
import random

class Miller_Rabin(PrimeTestTemplate):   
    def is_prime(self, digit, chance = float):
    # ----------- Проверка примитивных случаев -----------
        if digit == 2 or digit == 3:
            return True
        if digit <= 1 or digit % 2 == 0:
            return False
        # Представляем n - 1 в виде (2^r) * d
        r, d = 0, digit - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        iterations = miller_rabin_it_count(chance)
        # ------------------ Тест Миллера_Рабина-----------
        for _ in range(iterations):
            a = random.randint(2, digit - 2)
            x = pow_operations.pow_mod(a, d, digit)
            if x == 1 or x == digit - 1:
                continue
            for _ in range(r - 1):
                x = pow_operations.pow_mod(x, 2, digit)
                if x == digit - 1:
                    break
            else:
                return False

        return True