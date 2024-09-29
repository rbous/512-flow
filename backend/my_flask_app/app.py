# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from user import load_users, save_users

app = Flask(__name__)
CORS(app)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def create_db():
    """Create the database tables."""
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist


@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists."}), 400

    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    # Update users_data in user.py
    users_data = load_users()
    users_data[username] = {"password": password, "items": [], "accepted_by": None}  # Adjust as needed
    save_users(users_data)

    return jsonify({"message": "User created successfully!", "username": username}), 201


if __name__ == '__main__':
    create_db()  # Create the database tables when running the app
    app.run(debug=True)
