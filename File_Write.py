import binascii

def file_write(text, file_path):
    file = open(file_path, 'wb')
    file.write(text)
    file.close()

def save_hex_to_file(hex_String, filename):
    binary_data = binascii.unhexlify(hex_String)

    with open(filename, 'wb') as file:
        file.write(binary_data)

def write_list_to_file(file_path, lst):
    with open(file_path, 'w') as f:
        f.write(' '.join(map(str, lst)))

def write_list_to_file_final(file_path, lst):
    with open(file_path, 'w') as f:
        f.write(''.join(map(str, lst)))