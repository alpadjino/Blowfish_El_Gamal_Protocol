from One_Round import One_Round
from Fiestel import Feistel
from Common import split_bytearray, xor_hex_and_bytes

class ECB_Mode(Feistel):
    def feistel(self, block_bytes, sboxes, iteraton_keys, IV, feistel_mode: bool):
        left, right = split_bytearray(block_bytes) 

        if feistel_mode == True:
            for i in range(16):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[17], left)
            right = xor_hex_and_bytes(iteraton_keys[16], right)
        else:
            for i in range(17, 1, -1):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[0], left)
            right = xor_hex_and_bytes(iteraton_keys[1], right)

        return IV, left + right