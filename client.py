import socket
from config import CHUNK_SIZE

def request_chunk(node_ip, node_port, chunk_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((node_ip, node_port))
    client.send(b'request_chunk')
    client.send(str(chunk_id).encode())

    chunk = client.recv(CHUNK_SIZE)
    with open(f'chunk_{chunk_id}.part', 'wb') as f:
        f.write(chunk)
    client.close()
    print(f"Chunk {chunk_id} downloaded from {node_ip}:{node_port}")