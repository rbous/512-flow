from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User, db  # Import User and db from models.py

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\nabil\OneDrive\Desktop\Grocery Sharing\shopshare\backend\database.db'
app.config['SECRET_KEY'] = "thisisasecretkey"  # Secret key for session management

db.init_app(app)  # Initialize the database

login_manager = LoginManager(app)  # Initialize Flask-Login
login_manager.login_view = 'login'  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    full_name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Full Name"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Full Name"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")





