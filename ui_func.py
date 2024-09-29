
from backend.my_flask_app.models import db, User
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel,
    QMessageBox, QSizePolicy, QSpacerItem, QTextEdit, QListWidget, QComboBox
)
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
import requests

# Sample user data structure
users_data = {
    "user1": {"password": "pass1", "items": ["item1", "item2"], "accepted_by": None},
    "user2": {"password": "pass2", "items": ["item3", "item4"], "accepted_by": None},
    "user3": {"password": "pass3", "items": ["item5", "item6"], "accepted_by": None},
}


class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sign In')
        self.background_image = QPixmap('bg_gui.jpg')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.title_label = QLabel('Sign In', self)
        self.title_label.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        self.username_label = QLabel('Username:', self)
        self.username_label.setStyleSheet("color: black; font-weight: bold; font-size: 16px;")
        self.username_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.username_label, alignment=Qt.AlignCenter)

        self.username_input = QLineEdit(self)
        self.username_input.setStyleSheet(self.input_style())
        self.username_input.setFixedWidth(300)
        self.layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        self.password_label = QLabel('Password:', self)
        self.password_label.setStyleSheet("color: black; font-weight: bold; font-size: 16px;")
        self.password_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.password_label, alignment=Qt.AlignCenter)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        self.password_input.setFixedWidth(300)
        self.layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        self.create_button("Sign In", on_click=self.validate_credentials)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.create_button("Register", on_click=self.open_registration_window)

        # Add a QListWidget to display registered users
        self.user_list_widget = QListWidget(self)
        self.layout.addWidget(self.user_list_widget, alignment=Qt.AlignCenter)

        self.load_user_list()  # Load initial user list

    def open_registration_window(self):
        self.registration_window = RegistrationWindow(on_user_registered=self.load_user_list)
        self.registration_window.show()

    def load_user_list(self):
        self.user_list_widget.clear()
        self.user_list_widget.addItems(users_data.keys())


    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()

    def resizeEvent(self, event):
        self.set_background()

    def set_background(self):
        background = self.background_image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palette)

    def create_button(self, text, on_click=None):
        button = QPushButton(text, self)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setFixedSize(150, 40)
        button.setStyleSheet(self.button_style())

        if on_click:
            button.clicked.connect(on_click)

        self.layout.addWidget(button, alignment=Qt.AlignCenter)

    def validate_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        response = requests.post("http://127.0.0.1:5000/signin", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            self.open_item_entry_window(username)
        else:
            self.show_message('Error', 'Invalid username or password.')

    def open_item_entry_window(self, username):
        self.item_window = ItemEntryWindow(username)
        self.item_window.show()
        self.close()  # Close the sign-in window

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def input_style(self):
        return """
        QLineEdit {
            border: 2px solid gray;
            border-radius: 10px;
            padding: 5px;
            background-color: white;
            color: black;
        }
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #5cb85c;
            color: white;
            border-radius: 10px;
            font-size: 18px; 
            font-weight: bold; 
        }
        QPushButton:hover {
            background-color: #4cae4c;
        }
        """

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Register')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.username_label = QLabel('Username:', self)
        self.layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel('Password:', self)
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.create_button("Register", on_click=self.register_user)

    def create_button(self, text, on_click=None):
        button = QPushButton(text, self)
        button.clicked.connect(on_click)
        self.layout.addWidget(button)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        response = requests.post("http://127.0.0.1:5000/register", json={
            "username": username,
            "password": password
        })

        if response.status_code == 201:
            self.show_message('Success', 'User created successfully!')
            self.close()  # Close the registration window
        else:
            self.show_message('Error', response.json().get("message"))

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

class ItemEntryWindow(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.setWindowTitle(f'Item Entry - {self.username}')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel(f'Items for {self.username}', self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Dropdown to select which user's list to view
        self.user_selector = QComboBox(self)
        self.user_selector.addItems(users_data.keys())
        self.user_selector.currentTextChanged.connect(self.load_items)
        self.layout.addWidget(self.user_selector, alignment=Qt.AlignCenter)

        self.item_input = QTextEdit(self)
        self.item_input.setPlaceholderText("Enter items here, one per line...")
        self.layout.addWidget(self.item_input)

        self.create_button("Submit", on_click=self.submit_items)

        self.items_list_widget = QListWidget(self)
        self.layout.addWidget(self.items_list_widget)

        # Create Accept button (hidden initially)
        self.accept_button = QPushButton("Accept List", self)
        self.accept_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.accept_button.setFixedSize(150, 40)
        self.accept_button.setStyleSheet(self.button_style())
        self.accept_button.clicked.connect(self.accept_list)
        self.layout.addWidget(self.accept_button, alignment=Qt.AlignCenter)
        self.accept_button.hide()

        self.load_items()  # Load the current user's items

    def create_button(self, text, on_click=None):
        button = QPushButton(text, self)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setFixedSize(150, 40)
        button.setStyleSheet(self.button_style())

        if on_click:
            button.clicked.connect(on_click)

        self.layout.addWidget(button, alignment=Qt.AlignCenter)


    def submit_items(self):
        selected_user = self.user_selector.currentText()
        if selected_user == self.username:
            items = self.item_input.toPlainText().splitlines()
            if items:
                # Update the grocery list in the database
                user = User.query.filter_by(username=self.username).first()
                user.grocery_list = items  # Update the grocery list
                db.session.commit()  # Commit the changes to the database
                self.show_message('Success', 'Items submitted successfully!')
                self.load_items()
            else:
                self.show_message('Error', 'No items entered.')
        else:
            self.show_message('Error', 'You can only edit your own list.')

    def load_items(self):
        self.items_list_widget.clear()
        selected_user = self.user_selector.currentText()

        # Get the user's grocery list from the database
        user = User.query.filter_by(username=selected_user).first()
        if user:
            items = user.grocery_list  # Fetch the grocery list
            self.items_list_widget.addItems(items)

        if selected_user != self.username:
            self.item_input.setDisabled(True)
            if user.accepted_by is None:
                self.accept_button.show()
            else:
                self.accept_button.hide()  # Hide if already accepted
        else:
            self.item_input.setDisabled(False)
            self.accept_button.hide()

    def accept_list(self):
        selected_user = self.user_selector.currentText()
        if selected_user != self.username:
            if users_data[selected_user]["accepted_by"] is None:
                users_data[self.username]["items"].extend(users_data[selected_user]["items"])
                users_data[selected_user]["accepted_by"] = self.username  # Mark list as accepted by the current user
                self.show_message('Success', f'Accepted {selected_user}\'s list!')
                self.load_items()  # Reload the merged list
            else:
                self.show_message('Error',
                                  f'{selected_user}\'s list has already been accepted by {users_data[selected_user]["accepted_by"]}.')

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def button_style(self):
        return """
        QPushButton {
            background-color: #5cb85c;
            color: white;
            border-radius: 10px;
            font-size: 18px; 
            font-weight: bold; 
        }
        QPushButton:hover {
            background-color: #4cae4c;
        }
        """
