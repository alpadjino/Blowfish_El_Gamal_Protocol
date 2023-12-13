from Common import generate_close_key, split_bytearray, from_bytes_to_hex
from Cypher_Modes.ECB import ECB_Mode

class key_generate():
    def __init__(self, key: str, started_sboxes, started_keys, IV):
        self.key = generate_close_key(key)
        self.started_sboxes = started_sboxes.copy()
        self.started_keys = started_keys.copy()
        self.feistel = ECB_Mode
        self.IV = IV
        
    def Key_generate(self): 
        p = 0
        for i in range(18):
            self.started_keys[i] = self.started_keys[i] ^ from_bytes_to_hex(self.key[p: p + 4])
            p += 4

        zero_string = b'00000000'
        for i in range(0, 17, 2):
            self.IV, FS = self.feistel.feistel(self, zero_string, self.started_sboxes, self.started_keys, self.IV, 1)
            first, second = split_bytearray(FS)#split_bytearray(self.feistel.feistel(zero_string, self.started_sboxes, self.started_keys, 1))
            self.started_keys[i], self.started_keys[i + 1]  = from_bytes_to_hex(first), from_bytes_to_hex(second)
            zero_string = first + second    

        zero_string = b'00000000'
        for i in range(4):
            for j in range(0, 255, 2):
                self.IV, FS = self.feistel.feistel(self, zero_string, self.started_sboxes, self.started_keys, self.IV, 1)
                first, second = split_bytearray(FS)# split_bytearray(self.feistel.feistel(zero_string, self.started_sboxes, self.started_keys, 1))
                self.started_sboxes[i][j], self.started_sboxes[i][j + 1]  = from_bytes_to_hex(first), from_bytes_to_hex(second)
                zero_string = first + second
        return self.started_keys, self.started_sboxes