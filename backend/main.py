import sqlite3
from user import User
from grocerylist import GroceryList
from storage import storaging, fetch_data, clean_storage  # Assuming storaging and fetch_data are in storage.py

def main():
    storaging()

    while True:
        print("\nMenu:")
        print("1. View all stored data")
        print("2. Add new user")
        print("3. Create new grocery list")
        print("4. Clean storage")  # New option to clean storage
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            fetch_data()
        elif choice == '2':
            full_name = input("Enter your full name: ")
            user = User(full_name)
            user.save_to_db()
            print(f"User {full_name} added successfully.")
        elif choice == '3':
            full_name = input("Enter your full name: ")
            items_string = input("Enter grocery items (comma-separated): ")
            user = User(full_name)  # You might want to fetch the user from the database instead
            grocery_list = user.create_list(items_string)
            grocery_list.save_to_db()
            print(f"Grocery list created for {full_name}.")
        elif choice == '4':
            clean_storage()  # Call the clean_storage method
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()