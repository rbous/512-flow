from flask import Flask, request, jsonify
import sqlite3
from user import User
from grocerylist import GroceryList

app = Flask(__name__)

# Set up the database (similar to storaging)
def init_db():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
        lists(id INTEGER PRIMARY KEY, full_name STRING, tasks_lists STRING, collaborating STRING, collaborated INTEGER)"""
    
    command2 = """CREATE TABLE IF NOT EXISTS
        user_info(username STRING PRIMARY KEY)"""

    cursor.execute(command1)
    cursor.execute(command2)
    connections.commit()
    connections.close()
    
@app.route('/')
def home():
    return "Welcome to the Grocery Sharing API"

# Fetch all users
@app.route('/users', methods=['GET'])
def fetch_users():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()

    cursor.execute("SELECT * FROM user_info")
    users = cursor.fetchall()

    if users:
        user_data = [{"username": user[0]} for user in users]
        return jsonify({"users": user_data}), 200
    else:
        return jsonify({"message": "No users found."}), 404

# Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    full_name = data.get('full_name')

    if not full_name:
        return jsonify({"error": "Full name is required"}), 400

    user = User(full_name)
    try:
        user.save_to_db()
        return jsonify({"message": f"User {full_name} added successfully."}), 201
    except sqlite3.IntegrityError:  # Handle duplicate username
        return jsonify({"error": "User already exists"}), 400

# Fetch all grocery lists
@app.route('/grocery-lists', methods=['GET'])
def fetch_grocery_lists():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()

    cursor.execute("SELECT * FROM lists")
    grocery_lists = cursor.fetchall()

    if grocery_lists:
        list_data = []
        for grocery_list in grocery_lists:
            items_string = grocery_list[2]
            items_list = [item.strip() for item in items_string.split(",") if item.strip()]
            formatted_items = ', '.join(items_list)

            list_data.append({
                "list_id": grocery_list[0],
                "owner": grocery_list[1],
                "items": formatted_items,
                "collaborating": grocery_list[3],
                "collaborated": grocery_list[4]
            })
        return jsonify({"grocery_lists": list_data}), 200
    else:
        return jsonify({"message": "No grocery lists found."}), 404

# Create a new grocery list
@app.route('/grocery-lists', methods=['POST'])
def create_grocery_list():
    data = request.get_json()
    full_name = data.get('full_name')
    items = data.get('items')

    if not full_name or not items:
        return jsonify({"error": "Full name and items are required"}), 400

    # Create a new grocery list
    user = User(full_name)  # Optionally fetch user from DB
    grocery_list = user.create_list(items)

    # Save grocery list to database
    try:
        grocery_list.save_to_db()
        return jsonify({"message": f"Grocery list created for {full_name}."}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Clean the storage (delete all users and grocery lists)
@app.route('/clean-storage', methods=['DELETE'])
def clean_storage():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()

    cursor.execute("DELETE FROM user_info")
    cursor.execute("DELETE FROM lists")
    connections.commit()
    connections.close()

    return jsonify({"message": "Storage cleaned successfully."}), 200

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
