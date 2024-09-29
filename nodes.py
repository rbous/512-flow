import socket
import os
import threading
import config  # Ensure config has the CHUNK_SIZE defined
import time
import hashlib  # Import hashlib for hashing

peers = set()  # Use a set for unique connected peers
lock = threading.Lock()  # Lock for thread-safe access to peers list

def calculate_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(config.CHUNK_SIZE)
                if not data:
                    break
                sha256_hash.update(data)
    except FileNotFoundError:
        print(f"[-] File not found: {file_path}")
        return None
    except Exception as e:
        print(f"[-] An error occurred: {str(e)}")
        return None

    return sha256_hash.hexdigest()

def is_port_in_use(port):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('', port)) == 0

def get_local_ip():
    """Get the local IP address of the machine running the bootstrap node."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'  # Fallback in case of failure
    finally:
        s.close()
    return ip_address

def start_server(port):
    """Start the bootstrap server."""
    if is_port_in_use(port):
        print(f"Port {port} is already in use. Exiting.")
        return
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(30)

    bootstrap_ip = "192.168.250.105"
    print(f"Bootstrap node running at IP: {bootstrap_ip}, Port: {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} accepted.")
        threading.Thread(target=handle_client, args=(client_socket,)).start()  # Handle each client in a new thread

def handle_client(client_socket):
    """Handle communication with a connected client."""
    try:
        message = client_socket.recv(1024).decode().strip()
        if message.startswith("REGISTER"):
            peer_ip = message.split()[1]  # Extract IP address
            register_peer(peer_ip)
            client_socket.send(b"Registered successfully.")
        elif message == "REQUEST_PEERS":
            with lock:
                peers_list = ",".join(peers)
            client_socket.send(peers_list.encode())
        else:  # Handle file request
            print(f"Request for file: '{message}'")
            if os.path.exists(message):
                client_socket.send(b"OK")  # Indicate the file is found
                
                # Calculate the hash of the file
                file_hash = calculate_hash(message)
                client_socket.send(file_hash.encode())  # Send the hash to the client

                with open(message, 'rb') as f:
                    chunk = f.read(config.CHUNK_SIZE)
                    while chunk:
                        client_socket.sendall(chunk)
                        chunk = f.read(config.CHUNK_SIZE)
                print("File and hash sent successfully.")
            else:
                client_socket.send(b"File not found")
                print("File not found or filename was empty.")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def register_peer(peer_ip):
    """Register a new peer IP address."""
    with lock:
        peers.add(peer_ip)  # Using set to avoid duplicates
        print(f"Peer {peer_ip} registered.")

def client(peer_ip, peer_port, filename):
    """Download a file from a peer."""
    if not filename:  # Check if the filename is valid
        print("No filename provided for download.")
        return
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((peer_ip, peer_port))
        client_socket.send(filename.encode())  # Send the filename to request

        response = client_socket.recv(1024).decode()
        if response == "OK":
            # Receive the hash from the peer
            received_hash = client_socket.recv(64).decode()  # SHA-256 hash is 64 hex characters
            
            with open('downloaded_' + filename, 'wb') as f:
                while True:
                    chunk = client_socket.recv(config.CHUNK_SIZE)
                    if not chunk:
                        break  # Exit loop if no more data
                    f.write(chunk)
            print(f"File '{filename}' downloaded successfully.")

            # Verify the hash of the downloaded file
            calculated_hash = calculate_hash('downloaded_' + filename)
            if calculated_hash == received_hash:
                print("[+] Hash verification successful. The file is intact.")
            else:
                print("[-] Hash verification failed. The file may have been altered.")
        else:
            print(response)  # This will print "File not found"
    except Exception as e:
        print(f"Error while downloading file: {e}")
    finally:
        client_socket.close()

def attempt_to_connect(bootstrap_ip, bootstrap_port):
    """Try to connect to the bootstrap node."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  # Set a timeout for the connection attempt
        client_socket.connect((bootstrap_ip, bootstrap_port))
        print(f"Connected to bootstrap node at {bootstrap_ip}:{bootstrap_port}")

        # Send registration command with local IP
        local_ip = get_local_ip()
        registration_message = f"REGISTER {local_ip}"
        client_socket.send(registration_message.encode())
        return client_socket
    except (socket.timeout, ConnectionRefusedError):
        print("No bootstrap node found, starting as bootstrap.")
        return None

def refresh_peers(bootstrap_ip='192.168.250.105', bootstrap_port=5000):
    """Thread function to refresh peers list."""
    while True:
        try:
            # Attempt to connect to the bootstrap node to refresh the peers list
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((bootstrap_ip, bootstrap_port))
                s.send(b"REQUEST_PEERS")
                peers_data = s.recv(1024).decode()
                if peers_data:
                    with lock:
                        peers.clear()
                        peers.update(peers_data.split(","))  # Update the global peers list
                    print(f"Updated peers list: {peers}")

        except (socket.timeout, ConnectionRefusedError):
            print("Unable to connect to bootstrap to refresh peers.")
        
        time.sleep(60)  # Wait for a while before refreshing again

def start_node(bootstrap_ip='192.168.250.105', bootstrap_port=5000):
    """Main function to start the node."""
    bootstrap_connection = attempt_to_connect(bootstrap_ip, bootstrap_port)

    if bootstrap_connection is None:
        bootstrap_thread = threading.Thread(target=start_server, args=(bootstrap_port,))
        bootstrap_thread.start()  # Start the server in a separate thread
        print(f"Bootstrap node started on port {bootstrap_port}.")
        print("No peers available yet, this is the first node in the network.")
    else:
        print("Connected to an existing bootstrap node.")

    threading.Thread(target=refresh_peers, args=(bootstrap_ip, bootstrap_port), daemon=True).start()

    # Allow the user to enter file download requests
    while True:
        print("Enter 'd' to download a file or 'q' to quit:")
        choice = input().strip().lower()
        if choice == 'q':
            print("Exiting...")
            break
        elif choice == 'd':
            peer_ip = input("Enter the IP of the peer to download from: ")
            filename = input("Enter the filename to download: ")
            if filename:  # Only proceed if a filename is provided
                client(peer_ip, bootstrap_port, filename)
            else:
                print("Filename cannot be empty.")
        else:
            print("Invalid option. Please enter 'd' or 'q'.")

if __name__ == "__main__":
    start_node()  # Start the node which may act as bootstrap
