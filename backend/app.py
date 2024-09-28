from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

# Database configuration with a raw string for Windows
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\nabil\OneDrive\Desktop\Grocery Sharing\shopshare\backend\database.db'
app.config['SECRET_KEY'] = "thisisasecretkey"  # Secret key for session management

db = SQLAlchemy(app)  # Initialize the database

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # User ID
    username = db.Column(db.String(20), nullable=False, unique=True)  # Ensure username is unique
    password = db.Column(db.String(80), nullable=False)  # User password

# Create the database tables (do this once)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database and tables created!")
