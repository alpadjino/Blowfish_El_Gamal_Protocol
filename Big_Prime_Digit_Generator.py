from Big_Digit_Generator import big_digit_generator
from Ferma_Test import ferma_method
from Soloway_Strassen_method import Soloway_Strassen
from Miller_Rabin_Test import Miller_Rabin
from Enum_Class import Direction


def big_prime_digit_generator(method_name: Direction, chance: float, lenght: int):
    digit = big_digit_generator(lenght)

    if method_name == Direction.FERMA:
        ferma = ferma_method()
        while ferma.template_method(digit, chance) == False:
            digit = big_digit_generator(lenght)
        return digit

    elif method_name == Direction.SOLOWAY_STRASSEN:
        soloway = Soloway_Strassen()
        while soloway.template_method(digit, chance) == False:
            digit = big_digit_generator(lenght)
        return digit

    else:
        miller = Miller_Rabin()
        while miller.template_method(digit, chance) == False:
            digit = big_digit_generator(lenght)
        return digit
