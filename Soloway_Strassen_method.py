from Pow_Operations import pow_operations
from Template_Class import PrimeTestTemplate
from Jacobi_Lejandre_Service import NumberTheoryService
from Soloway_Strassen_Iteration_Count import soloway_strassen_it_count
import random

class Soloway_Strassen(PrimeTestTemplate):
    def is_prime(self, digit, chance = float):
        if digit == 2 or digit == 3:
            return True
        if digit == 1 or digit % 2 == 0:
            return False
        
        iterations = soloway_strassen_it_count(chance)
        for _ in range(iterations):
            a = random.randint(2, digit-1)
            x = NumberTheoryService.jacobian_symbol(a, digit)
            y = pow_operations.pow_mod(a, (digit-1)//2, digit)
            
            if x == 0 or y != x % digit:
                return False
        
        return True