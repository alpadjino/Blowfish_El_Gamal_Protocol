from Common import split_bytearray, from_bytes_to_hex, from_hex_to_bytes, xor_hex_and_bytes

def F(left, sboxes):
    first, second = split_bytearray(left)

    a, b = split_bytearray(first)
    c, d = split_bytearray(second)

    a = sboxes[0][from_bytes_to_hex(a)]
    b = sboxes[1][from_bytes_to_hex(b)]
    c = sboxes[2][from_bytes_to_hex(c)]
    d = sboxes[3][from_bytes_to_hex(d)]

    result = from_hex_to_bytes((a + b) % (2**32))
    result = xor_hex_and_bytes(c, result)
    result = from_hex_to_bytes(((from_bytes_to_hex(result) + d)) % (2**32))

    return result