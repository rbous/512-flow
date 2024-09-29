import socket
import os
import threading
import config  # Ensure config has the CHUNK_SIZE defined
import time

CHUNK_SIZE = 512
bootstrap_ip = '192.168.250.105'
bootstrap_port = 5000
peers = set()

def register_with_bootstrap():
    """Register this node with the bootstrap node."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((bootstrap_ip, bootstrap_port))

        # Send the IP to register
        local_ip = "192.168.104.140"
        client_socket.send(local_ip.encode())

        # Receive the list of peers
        peers_data = client_socket.recv(1024).decode()
        if peers_data:
            peers.update(peers_data.split(","))
            print(f"Received updated peers list: {peers}")

        client_socket.close()
    except Exception as e:
        print(f"Failed to register with bootstrap: {e}")

def handle_client(client_socket):
    """Handle communication with a connected client."""
    try:
        message = client_socket.recv(1024).decode().strip()
        print(f"Request for file: '{message}'")
        if os.path.exists(message):
            client_socket.send(b"OK")
            with open(message, 'rb') as f:
                chunk = f.read(CHUNK_SIZE)
                while chunk:
                    client_socket.sendall(chunk)
                    chunk = f.read(CHUNK_SIZE)
            print("File sent successfully.")
        else:
            client_socket.send(b"File not found")
            print("File not found.")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server(port):
    """Start the file-sharing server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(30)

    local_ip = "192.168.104.140"
    print(f"File-sharing node running at IP: {local_ip}, Port: {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} accepted.")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def client(peer_ip, peer_port, filename):
    """Download a file from a peer."""
    if not filename:
        print("No filename provided for download.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((peer_ip, peer_port))
        client_socket.send(filename.encode())

        response = client_socket.recv(1024).decode()
        if response == "OK":
            with open('downloaded_' + filename, 'wb') as f:
                while True:
                    chunk = client_socket.recv(CHUNK_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"File '{filename}' downloaded successfully.")
        else:
            print(response)
    except Exception as e:
        print(f"Error while downloading file: {e}")
    finally:
        client_socket.close()

def start_node():
    """Main function to start the node as a file-sharing node."""
    port = 5000  # Start file-sharing node on port 5001

    # Register with the bootstrap node
    register_with_bootstrap()

    # Start the file-sharing server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    print(f"Server running on port {port}")

    # Allow the user to enter file download requests
    while True:
        print("Enter 'd' to download a file or 'q' to quit:")
        choice = input().strip().lower()
        if choice == 'q':
            print("Exiting...")
            break
        elif choice == 'd':
            if peers:
                peer_ip = input("Enter the IP of the peer to download from: ")
                filename = input("Enter the filename to download: ")
                if filename:
                    client(peer_ip, port, filename)
                else:
                    print("Filename cannot be empty.")
            else:
                print("No peers available.")
        else:
            print("Invalid option. Please enter 'd' or 'q'.")

if __name__ == "__main__":
    start_node()
