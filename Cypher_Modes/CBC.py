from One_Round import One_Round
from Common import split_bytearray, xor_hex_and_bytes, xor_bytes
from Fiestel import Feistel

class CBC_Mode(Feistel):
    def feistel(self, block_bytes, sboxes, iteraton_keys, IV, feistel_mode: bool):

        if feistel_mode == True:
            block_bytes = xor_bytes(block_bytes, IV)
            left, right = split_bytearray(block_bytes) 

            for i in range(16):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[17], left)
            right = xor_hex_and_bytes(iteraton_keys[16], right)

            IV = left + right
        else:
            started_bytes = block_bytes

            for i in range(17, 1, -1):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[0], left)
            right = xor_hex_and_bytes(iteraton_keys[1], right)

            left, right = (split_bytearray(xor_bytes(left + right, IV)))
            IV = started_bytes

        return IV, left + right