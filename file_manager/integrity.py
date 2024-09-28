import hashlib

def hash_file(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def verify_file_integrity(original_file, downloaded_file):
    original_hash = hash_file(original_file)
    downloaded_hash = hash_file(downloaded_file)
    return original_hash == downloaded_hash