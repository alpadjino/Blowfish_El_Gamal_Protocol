# ------------------ Из строки в байты ----------------------------
def from_string_to_bytes(string):
    string_bytes = bytes(string, "UTF-8")

    return string_bytes
# ---------------- xor байтов -------------------------------------
def xor_bytes(one, two):
    xor_bytes = bytes(a ^ b for (a, b) in zip(one, two))

    return xor_bytes
# ------------- Разбивает байтовую строку на 2 равные -------------
def split_bytearray(byte):
    length = len(byte)
    mid = length // 2

    return byte[:mid], byte[mid:]
# ----------------- Из 16 СС в строку байтов ----------------------
def from_hex_to_bytes(hex_digit):
    hex_val = hex(hex_digit)[2:]
    return bytes([int(hex_val[i : i + 2], 16) for i in range(0, len(hex_val), 2)])
# ---------------- Соединяет байты в 1 строку ---------------------
def connect_bytes(a, b):
    return b"".join([a, b])

# ---------------- xor байтов и 16 СС -----------------------------
def xor_hex_and_bytes(hex_digit, byte_array):
    return xor_bytes(from_hex_to_bytes(hex_digit), byte_array)

# ---------------- Создает заданный закрытый ключ в 72 байта ------
def generate_close_key(key: str):
    key = from_string_to_bytes(key)
    if (len(key) > 56):
        print("Key must be: 4 <= key <= 56 ")
    while len(key) < 72:
        key = connect_bytes(key, key)

    return key[:72]

def from_bytes_to_hex(byte_array):
    return int.from_bytes(byte_array, byteorder='big')

def increment_byte(byte_string, counter):
    int_b = int.from_bytes(byte_string, byteorder='big')
    int_b += counter
    return int_b.to_bytes(len(byte_string), byteorder='big')

def bytes_to_bits(byte_string):
    bits = ''.join(format(byte, '08b') for byte in byte_string)
    return bits

def bits_to_bytes(bit_string):
    byte_string = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = int(bit_string[i:i+8], 2)
        byte_string.append(byte)
    return byte_string

def shift_key(key, shift):
    key = bytes_to_bits(key)
    
    left_part = key[:len(key)//2]
    right_part = key[len(key)//2:]

    shifted_left_part = left_part[shift:] + left_part[:shift]
    shifted_right_part = right_part[shift:] + right_part[:shift]
    return bits_to_bytes(shifted_left_part + shifted_right_part)