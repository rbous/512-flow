import argparse
import hashlib
import sys

# Function to calculate the SHA-256 hash of a file.
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            # Read the file in 512-byte chunks.
            while True:
                data = file.read(512)
                if not data:
                    break
                sha256_hash.update(data)
    except FileNotFoundError:
        print(f"[-] File not found: {file_path}")
        sys.exit()
    except Exception as e:
        print(f"[-] An error occurred: {str(e)}")
        sys.exit()

    return sha256_hash.hexdigest()

# Command-line argument parsing.
parser = argparse.ArgumentParser(description="Calculate SHA-256 hash of a file.")
parser.add_argument("-f", "--file", dest="file_path", required=True,
                    help="Path of the file to hash")
args = parser.parse_args()

# Calculate and print the hash.
expected_hash = calculate_hash(args.file_path)
print(f"The SHA-256 hash of the file is: {expected_hash}")
