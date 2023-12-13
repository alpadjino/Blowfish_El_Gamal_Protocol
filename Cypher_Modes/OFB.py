from One_Round import One_Round
from Common import split_bytearray, xor_hex_and_bytes, xor_bytes
from Fiestel import Feistel

class OFB_Mode(Feistel):
    def feistel(self, block_bytes, sboxes, iteraton_keys, IV, feistel_mode: bool):
        if feistel_mode == True:
            final_IV = IV
            IV, block_bytes = block_bytes, IV
            #--------------- blowfish encryption --------------------
            for i in range(16):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[17], left)
            right = xor_hex_and_bytes(iteraton_keys[16], right)
            #-------------- blowfish encryption end -----------------
            result = xor_bytes(left + right, IV)
            IV = final_IV
        else:
            final_IV = IV
            IV, block_bytes = block_bytes, IV
            #--------------- blowfish encryption --------------------
            for i in range(16):
                block_bytes = One_Round.one_round(i, block_bytes, sboxes, iteraton_keys)

            left, right = split_bytearray(block_bytes)
            left, right = right, left

            left = xor_hex_and_bytes(iteraton_keys[17], left)
            right = xor_hex_and_bytes(iteraton_keys[16], right)
            #-------------- blowfish encryption end -----------------
            result = xor_bytes(left + right, IV)
            IV = final_IV

        return IV, result