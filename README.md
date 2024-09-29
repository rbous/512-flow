# 2<sup>9</sup> Flow

This project was created in the context of Ciena's P2P Challenge at Hack The Hill II

A basic peer-to-peer (P2P) file-sharing protocol using the TCP/IP networking stack. 
This system allows nodes to share and request files with each other, chunked into 512-byte pieces for transfer. 
The project demonstrates how peers can broadcast their presence, discover other peers, and share files directly without a central server.

## Features
- File chunking into 512-byte pieces
- Peer discovery using UDP broadcasting
- Peer-to-peer file transfer over TCP
- Integrity checking using MD5 hash

## Requirements
- Python 3.x
- `tempfile`, `hashlib`, `socket`, `threading` and `os` libraries (all included in Python's standard library)

## Installation

```sh
$ git clone https://github.com/rbous/512-flow.git
$ cd 512-flow
```
## Usage

1. On the designated bootstrap machine, create bootstrap node.

```sh
$ python3 `bootstrap_registry.py`
$ python3 `bootstrap_node.py`
```

2. On any other machines, create additional nodes.

```sh
$ python3 `nodes.py`
```

3. On each node, enter ip adress of node, then file name as prompted.

> Files to be transferred must already be saved in the root folder of the targeted node.

### Example

```sh
# Background Process
$ python3 bootstrap_registry.py 
Bootstrap node running at IP: 192.168.250.105, Port: 5000
Waiting for peers to connect...
Peer connected: ('192.168.240.1', 62069)
Registered peer: 192.168.104.140
Peer connected: ('192.168.240.1', 62081)
Registered peer: 192.168.104.10


# Node A
$ python3 bootstrap_node.py      
Received updated peers list: {'Peers updated.'}
Server running on port 5000
File-sharing node running at IP: 192.168.104.140, Port: 5000
Enter 'd' to download a file or 'q' to quit:
Connection from ('192.168.104.10', 49998) accepted.
Request for file: 'test.txt'
File and hash sent successfully.


# Node B
$ python3 nodes.py
No bootstrap node found, starting as bootstrap.
Bootstrap node started on port 5000.
No peers available yet, this is the first node in the network.
Bootstrap node running at IP: 192.168.250.105, Port: 5000
Enter 'd' to download a file or 'q' to quit:
d
Enter the IP of the peer to download from: 192.168.104.140
Enter the filename to download: test2.txt
File 'test.txt' downloaded successfully.
[+] Hash verification successful. The file is intact.
Enter 'd' to download a file or 'q' to quit:
```



   
