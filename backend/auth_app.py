import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
)

class AuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Authentication")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)
        self.layout.addWidget(self.register_button)

        self.signin_button = QPushButton("Sign In", self)
        self.signin_button.clicked.connect(self.sign_in_user)
        self.layout.addWidget(self.signin_button)

        self.response_label = QLabel(self)
        self.layout.addWidget(self.response_label)

        self.setLayout(self.layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        response = requests.post("http://localhost:5000/register", json={
            "username": username,
            "password": password
        })

        if response.status_code == 201:
            QMessageBox.information(self, "Success", "User created successfully!")
        elif response.status_code == 400:
            QMessageBox.warning(self, "Error", "User already exists.")
        else:
            QMessageBox.critical(self, "Error", "Registration failed.")

    def sign_in_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        response = requests.post("http://localhost:5000/signin", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Login successful!")
        elif response.status_code == 401:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
        else:
            QMessageBox.critical(self, "Error", "Login failed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.exit(app.exec_())
