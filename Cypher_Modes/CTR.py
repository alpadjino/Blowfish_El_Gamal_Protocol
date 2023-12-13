from One_Round import One_Round
from Common import split_bytearray, xor_hex_and_bytes, xor_bytes, increment_byte
from Fiestel import Feistel

class CTR_Mode(Feistel):
    def feistel(self, block_bytes, sboxes, iteraton_keys, IV, feistel_mode: bool):

        if feistel_mode == True:
            started_IV = IV
            for i in range(16):
                IV = One_Round.one_round(i, IV, sboxes, iteraton_keys)

            left, right = split_bytearray(IV)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[17], left)
            right = xor_hex_and_bytes(iteraton_keys[16], right)
            block_bytes = xor_bytes(left + right, IV)
            IV = increment_byte(started_IV, 1)
        else:
            started_IV = IV
            for i in range(17, 1, -1):
                IV = One_Round.one_round(i, IV, sboxes, iteraton_keys)

            left, right = split_bytearray(IV)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[0], left)
            right = xor_hex_and_bytes(iteraton_keys[1], right)
            block_bytes = xor_bytes(left + right, IV)

            IV = increment_byte(started_IV, -1)

        return IV, block_bytes