CHUNK_SIZE = 512

def split_file(file_obj):
    chunks = []
    while True:
        chunk = file_obj.read(CHUNK_SIZE)
        if not chunk:
            break
        chunks.append(chunk)
    return chunks

def reconstruct_file(filename):
    pass # make later
    
    print(f"File {filename} reconstructed from downloaded chunks.")