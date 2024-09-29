import argparse
import hashlib
import sys

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
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
parser = argparse.ArgumentParser(description="Verify the integrity of a downloaded file.")
parser.add_argument("-f", "--file", dest="downloaded_file", required=True,
                    help="Path of the downloaded file")
parser.add_argument("--hash", dest="expected_hash", required=True,
                    help="Expected SHA-256 hash value")
args = parser.parse_args()

# Calculate the hash of the downloaded file.
calculated_hash = calculate_hash(args.downloaded_file)

# Verify and print the result.
if calculated_hash == args.expected_hash:
    print("[+] Hash verification successful. The file is intact.")
else:
    print("[-] Hash verification failed. The file may have been altered.")
