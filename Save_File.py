def save_data_to_file(binary_data, filename):
    with open(filename, 'wb') as file:
        file.write(binary_data)