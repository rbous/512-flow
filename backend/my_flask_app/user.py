# users.py

import json
import os

# File to persist user data
USERS_DATA_FILE = 'users_data.json'

# Load existing user data
def load_users():
    if os.path.exists(USERS_DATA_FILE):
        with open(USERS_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save user data
def save_users(users_data):
    with open(USERS_DATA_FILE, 'w') as f:
        json.dump(users_data, f)

# Initialize user data
users_data = load_users()
