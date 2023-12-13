from Nod_Operation import nod_operation
from Pow_Operations import pow_operations
from Template_Class import PrimeTestTemplate
from Ferma_Iteration_Count import ferma_iteration_count
import random


class ferma_method(PrimeTestTemplate):
    def is_prime(self, digit, chance=float):
        iterations = ferma_iteration_count(chance)
        for _ in range(iterations):
            a = random.randint(2, digit - 1)

            if nod_operation.get_nod(a, digit) != 1:
                return False
            if pow_operations.pow_mod(a, digit - 1, digit) != 1:
                return False
        return True