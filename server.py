import socket
import threading
from chunking import send_chunk, receive_chunk

def start_server(node_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', node_port))
    server.listen(5)
    print(f"Node server started on port {node_port}")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    command = client_socket.recv(1024).decode()
    if command == 'request_chunk':
        send_chunk(client_socket)
    elif command == 'upload_chunk':
        receive_chunk(client_socket)
    client_socket.close()