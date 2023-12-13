from One_Round import One_Round
from Common import split_bytearray, xor_hex_and_bytes, xor_bytes, shift_key
from Fiestel import Feistel

class CFB_Mode(Feistel):
    def feistel(self, block_bytes, sboxes, iteraton_keys, IV, feistel_mode: bool):
        if feistel_mode == True:
            IV, block_bytes = block_bytes, IV
            for i in range(16):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[17], left)
            right = xor_hex_and_bytes(iteraton_keys[16], right)
            block_bytes = left + right
            block_bytes = shift_key(block_bytes, 2)

            left, right = split_bytearray(xor_bytes(block_bytes, IV))
            IV = block_bytes
        else:
            IV, block_bytes = block_bytes, IV
            for i in range(16):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[17], left)
            right = xor_hex_and_bytes(iteraton_keys[16], right)
            block_bytes = left + right
            block_bytes = shift_key(block_bytes, 2)

            left, right = split_bytearray(xor_bytes(block_bytes, IV))
            IV = block_bytes
        return IV, left + right