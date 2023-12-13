import random

class Create_IV:
    def generate_random_iv(length):
        return bytes([random.randint(0, 255) for _ in range(length)])