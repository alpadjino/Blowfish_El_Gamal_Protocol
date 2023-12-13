import binascii

def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:  
            binary_data = file.read()
        return binascii.hexlify(binary_data)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))

def read_file_to_list(file_path):
    with open(file_path, 'r') as f:
        data = f.read().split()
    data = list(map(int, data))
    return data

def chunk_reader(fp, chunk_size):
    prev_chunk = fp.read(chunk_size)
    while True:
        next_chunk = fp.read(chunk_size)
        if not next_chunk:
            yield prev_chunk, True
            break
        yield prev_chunk, False
        prev_chunk = next_chunk