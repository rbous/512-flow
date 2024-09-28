import socket
import threading
import random
import time
from network.server import start_server
from network.client import request_chunk
from network.bootstrap import register_with_bootstrap, get_known_nodes
from file_manager.chunking import chunk_file, send_chunk, receive_chunk
from config import CHUNK_SIZE

class Node:
    def __init__(self, port):
        self.port = port
        self.chunks = []  # Store chunk IDs that the node owns
        self.peers = []   # List of known peers (IP, port)

    def start(self):
        # Register the node with the bootstrap server and discover other nodes
        self.peers = register_with_bootstrap(self.port)
        print(f"Discovered peers: {self.peers}")

        # Start the server to listen for incoming connections
        threading.Thread(target=start_server, args=(self.port,)).start()

        # Start requesting chunks from peers
        self.request_missing_chunks()

    def request_missing_chunks(self):
        """Logic for requesting missing file chunks from peers"""
        missing_chunks = self.find_missing_chunks()
        for chunk_id in missing_chunks:
            peer = random.choice(self.peers)  # Randomly pick a peer
            print(f"Requesting chunk {chunk_id} from {peer}")
            request_chunk(peer[0], peer[1], chunk_id)
            time.sleep(1)  # Add delay between requests

    def find_missing_chunks(self):
        """Return a list of missing chunk IDs that this node doesn't have"""
        all_chunks = set(range(1, 9))  # Assuming 8 chunks in the file
        return list(all_chunks - set(self.chunks))

if __name__ == "__main__":
    # Start a new node with a random port between 5001 and 5004
    port = random.randint(5001, 5004)
    node = Node(port)
    node.start()
