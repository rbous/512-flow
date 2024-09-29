import socket
import threading

peers = set()

def handle_peer(client_socket):
    """Handles peer connections to register and retrieve peers."""
    try:
        peer_ip = client_socket.recv(1024).decode().strip()
        if peer_ip:
            peers.add(peer_ip)
            print(f"Registered peer: {peer_ip}")
            client_socket.send(b"Peers updated.")

            # Send the updated list of peers
            peers_list = ",".join(peers)
            client_socket.send(peers_list.encode())
        else:
            client_socket.send(b"Invalid peer IP.")
    except Exception as e:
        print(f"Error handling peer: {e}")
    finally:
        client_socket.close()

def run_bootstrap():
    # Set up the bootstrap server
    bootstrap_ip = "192.168.250.105"
    port = 5000
    print(f"Bootstrap node running at IP: {bootstrap_ip}, Port: {port}")
    
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((bootstrap_ip, port))
    server_socket.listen(5)  # Listen for up to 5 peers at once
    
    print("Waiting for peers to connect...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Peer connected: {client_address}")
        threading.Thread(target=handle_peer, args=(client_socket,)).start()

if __name__ == '__main__':
    run_bootstrap()
