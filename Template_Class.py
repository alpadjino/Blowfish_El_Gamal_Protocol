from abc import ABC, abstractmethod

class PrimeTestTemplate(ABC):

    @abstractmethod
    def is_prime(self, digit, chance=float):
        pass

    def template_method(self, digit, chance: float):
        return self.is_prime(digit, chance)