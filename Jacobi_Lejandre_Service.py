from Pow_Operations import pow_operations

class NumberTheoryService:
    def legendre_symbol(a, p):
        # Проверяем простоту p
        if p % 2 == 0 or pow_operations.pow_mod(a, (p - 1) // 2, p) != 1:
            return -1
        # Инициализируем значение символа Лежандра
        legendre = 1
        # Применяем алгоритм обратной записи числа p в двоичном виде
        # исключая старший бит (значение 2**k)
        k = 0
        q = (p - 1) // 2

        while q % 2 == 0:
            q //= 2
            k += 1
        # Вычисляем символ Лежандра путем итеративного возведения в степень
        b = pow_operations.pow_mod(a, q, p)
        if b == 1 or b == p - 1:
            return legendre

        for _ in range(k):
            b = pow_operations.pow_mod(b, 2, p)
            if b == p - 1:
                return legendre

            legendre *= -1

        return 0   
    def jacobian_symbol(a, n):
        if n <= 0 or n % 2 == 0:
            return "n должно быть положительным нечетным числом"
        if a == 0:
            return 0
        if a == 1: 
            return 1
        result = 1
        while a != 0:
            while a % 2 == 0:
                a //= 2
                if n % 8 == 3 or n % 8 == 5:
                    result = -result
            a, n = n, a

            if a % 4 == 3 and n % 4 == 3:
                result = -result
            a %= n
        if n == 1:
            return result
        else:
            return 0       