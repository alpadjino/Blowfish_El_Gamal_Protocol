class pow_operations():
    def pow_mod(a: int, k: int, m: int):
        res = 1
        a = a % m
        while k > 0:
            if k % 2 == 1:
                res = (res * a) % m
            k //= 2
            a = (a ** 2) % m
        return res
       
    def my_pow(base, exponent):
        result = 1
        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2
        return result