import socket
import threading

known_nodes = []  # List of registered nodes

def bootstrap_server(port=5555):
    """Centralized server that registers and tracks all nodes"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print("Bootstrap node running...")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    """Handles registration of new nodes and shares the list of known nodes"""
    new_node_info = client_socket.recv(1024).decode()
    known_nodes.append(tuple(new_node_info.split(":")))
    print(f"Registered new node: {new_node_info}")

    # Send the list of known nodes back to the new node
    client_socket.send(str(known_nodes).encode())
    client_socket.close()

def register_with_bootstrap(node_port):
    """Register the current node with the bootstrap server and get the list of known nodes"""
    bootstrap_ip = '127.0.0.1'  # Assuming bootstrap is on localhost
    bootstrap_port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((bootstrap_ip, bootstrap_port))

    # Send node info to bootstrap
    client.send(f"127.0.0.1:{node_port}".encode())

    # Receive list of known nodes
    known_nodes = eval(client.recv(1024).decode())
    client.close()
    return known_nodes