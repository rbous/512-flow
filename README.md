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
git clone https://github.com/rbous/512-flow.git
cd 512-flow
```
## Usage
