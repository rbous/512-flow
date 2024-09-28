import os
from config import CHUNK_SIZE

def chunk_file(file_path):
    chunks = []
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)  # Read 512 bytes
            if not chunk:
                break
            chunks.append(chunk)
    return chunks

def send_chunk(client_socket):
    chunk_id = client_socket.recv(1024).decode()
    chunk_file = f'chunk_{chunk_id}.part'
    
    with open(chunk_file, 'rb') as f:
        chunk = f.read(CHUNK_SIZE)
        client_socket.send(chunk)
    print(f"Sent chunk {chunk_id}")

def receive_chunk(client_socket):
    chunk_id = client_socket.recv(1024).decode()
    chunk_data = client_socket.recv(CHUNK_SIZE)
    with open(f'chunk_{chunk_id}.part', 'wb') as f:
        f.write(chunk_data)
    print(f"Received chunk {chunk_id}")