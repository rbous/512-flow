from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user import User
from grocerylist import GroceryList
from app import db, LoginForm, RegisterForm  # Import the db and forms from app.py
import sqlite3
import secrets  # Import secrets to generate a secret key

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Set your secret key

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Use full_name instead of username
        new_user = User(full_name=form.username.data)  # Assuming you're using the same field for full_name
        new_user.set_password(form.password.data)  # Store the hashed password
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(full_name=form.full_name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Login Unsuccessful. Please check full name and password", "danger")
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Welcome, {current_user.username}!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/grocerylists')
@login_required  # Ensure user is logged in to view grocery lists
def grocery_lists():
    return render_template('list.html')

# Ensure tables exist
def storaging():
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()
    
    # Creating tables for users and lists
    command1 = """CREATE TABLE IF NOT EXISTS
        lists(id INTEGER PRIMARY KEY, full_name STRING, tasks_lists STRING, collaborating STRING, collaborated INTEGER)"""
    
    command2 = """CREATE TABLE IF NOT EXISTS
        user_info(username STRING PRIMARY KEY)"""
    
    cursor.execute(command1)
    cursor.execute(command2)
    connections.commit()
    connections.close()

storaging()  # Initialize the database

# Store users and grocery lists in-memory for this example
users = {}

# Create a new user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    full_name = data.get('full_name')
    
    if full_name in users:
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(full_name)
    users[full_name] = new_user
    new_user.save_to_db()
    
    return jsonify({"message": f"User {full_name} created successfully"}), 201

# Create a grocery list for a user
@app.route('/user/<username>/grocerylist', methods=['POST'])
def create_grocery_list(username):
    if username not in users:
        return jsonify({"message": "User not found"}), 404
    
    user = users[username]
    data = request.json
    items = data.get('items', "")
    
    grocery_list = user.create_list(items)
    grocery_list.save_to_db()
    
    return jsonify({"message": "Grocery list created successfully", "list": grocery_list.items}), 201

# Add items to a grocery list
@app.route('/grocerylist/<int:list_id>/add', methods=['POST'])
def add_items_to_grocery_list(list_id):
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()
    
    cursor.execute("SELECT * FROM lists WHERE id=?", (list_id,))
    list_data = cursor.fetchone()
    
    if not list_data:
        return jsonify({"message": "Grocery list not found"}), 404
    
    # Add items to the list
    grocery_list = GroceryList(users[list_data[1]], list_data[2].split(","))
    data = request.json
    new_items = data.get('items', "")
    
    grocery_list.addItems(new_items)
    grocery_list.save_to_db()  # Update the DB
    
    return jsonify({"message": "Items added successfully", "list": grocery_list.items}), 200

# Remove items from a grocery list
@app.route('/grocerylist/<int:list_id>/remove', methods=['POST'])
def remove_items_from_grocery_list(list_id):
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()
    
    cursor.execute("SELECT * FROM lists WHERE id=?", (list_id,))
    list_data = cursor.fetchone()
    
    if not list_data:
        return jsonify({"message": "Grocery list not found"}), 404
    
    # Remove items from the list
    grocery_list = GroceryList(users[list_data[1]], list_data[2].split(","))
    data = request.json
    items_to_remove = data.get('items', "")
    
    grocery_list.remove_items(items_to_remove)
    grocery_list.save_to_db()  # Update the DB
    
    return jsonify({"message": "Items removed successfully", "list": grocery_list.items}), 200

# Collaborate on a grocery list
@app.route('/grocerylist/<int:list_id>/collaborate', methods=['POST'])
def collaborate_on_list(list_id):
    data = request.json
    collaborator_name = data.get('collaborator')
    
    if collaborator_name not in users:
        return jsonify({"message": "Collaborator not found"}), 404
    
    collaborator = users[collaborator_name]
    
    connections = sqlite3.connect("clients.db")
    cursor = connections.cursor()
    
    cursor.execute("SELECT * FROM lists WHERE id=?", (list_id,))
    list_data = cursor.fetchone()
    
    if not list_data:
        return jsonify({"message": "Grocery list not found"}), 404
    
    # Collaborate on the list
    grocery_list = GroceryList(users[list_data[1]], list_data[2].split(","))
    grocery_list.add_collaborator(collaborator)
    grocery_list.save_to_db()
    
    return jsonify({"message": f"{collaborator_name} is now collaborating on the list", "list": grocery_list.items}), 200

if __name__ == '__main__':
    app.run(debug=True)
