import sqlite3
from user import User
from grocerylist import GroceryList

def storaging():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
        lists(id INTEGER PRIMARY KEY, full_name STRING, tasks_lists STRING, collaborating STRING, collaborated INTEGER)"""
    
    command2 = """CREATE TABLE IF NOT EXISTS
        user_info(username STRING PRIMARY KEY)"""

    cursor.execute(command1)
    cursor.execute(command2)
    connections.commit()
    return connections

def clean_storage():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()

    # Delete all rows from user_info
    cursor.execute("DELETE FROM user_info")
    
    # Delete all rows from lists
    cursor.execute("DELETE FROM lists")
    
    connections.commit()
    connections.close()
    print("Storage cleaned successfully.")


def fetch_data():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()

    # Fetch user info
    cursor.execute("SELECT * FROM user_info")
    users = cursor.fetchall()
    
    if users:
        print("User Info:")
        for user in users:
            print(f"Username: {user[0]}")  # Improve formatting
    else:
        print("No users found.")

    # Fetch grocery lists
    cursor.execute("SELECT * FROM lists")
    grocery_lists = cursor.fetchall()
    
    if grocery_lists:
        print("Grocery Lists:")
        for grocery_list in grocery_lists:
            # Get the items string from the database
            items_string = grocery_list[2]
            # Split and clean the items
            items_list = [item.strip() for item in items_string.split(",") if item.strip()]  # Clean and split
            
            # Join the items with a comma and space
            formatted_items = ', '.join(items_list) 
            print(f"List ID: {grocery_list[0]}, Owner: {grocery_list[1]}, Items: {formatted_items}, Collaborating: {grocery_list[3]}, Collaborated: {grocery_list[4]}")
    else:
        print("No grocery lists found.")

    connections.close()
