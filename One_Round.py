from Common import split_bytearray, xor_hex_and_bytes, xor_bytes
from F import F

class One_Round:
    def one_round(iteration, block_bytes, sboxes, iteraton_keys):
        left, right = split_bytearray(block_bytes)
        left = xor_hex_and_bytes(iteraton_keys[iteration], left)
        right = xor_bytes(F(left, sboxes), right)
        left, right = right, left

        return left + right