from Start_Values import keys, sbox0, sbox1, sbox2, sbox3
from Blowfish_Mode import blowfish_mode
from Key_Generate import key_generate
from Cypher_Modes.CBC import CBC_Mode
from Cypher_Modes.ECB import ECB_Mode
from Cypher_Modes.CFB import CFB_Mode
from Cypher_Modes.OFB import OFB_Mode

class Blowfish:
    def __init__(self, key: str, IV, bw_mode = blowfish_mode.ECB):
        sboxes = [list(sbox0), list(sbox1), list(sbox2), list(sbox3)]
        started_sboxes, started_keys = list(sboxes), list(keys)
        self.iteration_keys, self.sboxes = key_generate(key, started_sboxes, started_keys, IV).Key_generate()
        self.IV = IV
       
        if (bw_mode == blowfish_mode.ECB):
            self.objectMode = ECB_Mode()
        elif (bw_mode == blowfish_mode.CBC):
            self.objectMode = CBC_Mode()
        elif (bw_mode == blowfish_mode.CFB):
            self.objectMode = CFB_Mode()
        elif (bw_mode == blowfish_mode.OFB):
            self.objectMode = OFB_Mode()

    def encrypt(self, chunk):
        started_IV = self.IV       
        self.IV, chunk = self.objectMode.feistel(chunk, self.sboxes, self.iteration_keys, self.IV, 1)          
        self.IV = started_IV
        return self.IV, chunk

    def decrypt(self, chunk): 
        self.IV, chunk = self.objectMode.feistel(chunk, self.sboxes, self.iteration_keys, self.IV, 0)

        return chunk