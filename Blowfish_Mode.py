from enum import Enum

class blowfish_mode(Enum):
    ECB = "ecb"
    CBC = "cbc"
    CFB = "cfb"
    OFB = "ofb"