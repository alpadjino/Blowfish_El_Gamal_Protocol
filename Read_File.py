def chunk_reader(fp, chunk_size):
    prev_chunk = fp.read(chunk_size)
    while True:
        next_chunk = fp.read(chunk_size)
        if not next_chunk:
            yield prev_chunk, True
            break
        yield prev_chunk, False
        prev_chunk = next_chunk