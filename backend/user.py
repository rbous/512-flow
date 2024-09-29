import sqlite3
from grocerylist import GroceryList

class User:
    def __init__(self, full_name, created_list=None, help_list=None):
        if created_list is None:
            created_list = []
        if help_list is None:
            help_list = []
        self.created_list = created_list
        self.full_name = full_name
        self.help_list = help_list

    def create_list(self, items = (str)):
        new_list = GroceryList(self, items.split(","))
        self.created_list.append(new_list)
        return new_list  # Return the new list for further operations

    def save_to_db(self):
        connections = sqlite3.connect("clients.db")
        cursor = connections.cursor()
        cursor.execute("INSERT INTO user_info (username) VALUES (?)", (self.full_name,))
        connections.commit()
        connections.close()

    def __str__(self):
        return f'User: {self.full_name}'