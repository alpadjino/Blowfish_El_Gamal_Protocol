from File_Reader import read_file_to_list, chunk_reader
from File_Write import write_list_to_file, write_list_to_file_final

class el_gamal():
    def encrypt(p: int, g, y, k, file_path_to_read, file_path_to_save):
        # message = chunk_reader(file_path_to_read)
        encrypted_message = []
        with open(file_path_to_read, "rb") as file:
            for chunk, is_last in chunk_reader(file, 1):
                char = int.from_bytes(chunk)
                u = pow(g, k, p)
                v = (char % p) * (pow(y, k, p))
                encrypted_message.append(u)
                encrypted_message.append(v)
        write_list_to_file(file_path_to_save, encrypted_message)

    def decrypt(p: int, x, file_path_to_read, file_path_to_save):
        encrypt_message = read_file_to_list(file_path_to_read)
        decrypt_message = []
        for i in range(0, len(encrypt_message), 2):
            m = ((encrypt_message[i + 1] % p) * pow(encrypt_message[i], p - 1 - x, p)) % p
            decrypt_message.append(chr(m))
        write_list_to_file_final(file_path_to_save, decrypt_message)