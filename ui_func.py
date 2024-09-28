# button_creator.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel,
    QMessageBox, QSizePolicy, QSpacerItem, QTextEdit
)
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt


class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sign In')
        self.background_image = QPixmap('bg_gui.jpg')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add a spacer to push elements to the center
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

        # Add another spacer to push elements to the center
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

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

        if username == 'user' and password == 'pass':
            self.open_item_entry_window()  # Open the item entry window
        else:
            self.show_message('Error', 'Invalid username or password.')

    def open_item_entry_window(self):
        self.item_window = ItemEntryWindow()
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


class ItemEntryWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Item Entry')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel('Enter Your Items', self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        self.item_input = QTextEdit(self)
        self.item_input.setPlaceholderText("Enter items here, one per line...")
        self.layout.addWidget(self.item_input)

        self.create_button("Submit", on_click=self.submit_items)

    def create_button(self, text, on_click=None):
        button = QPushButton(text, self)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setFixedSize(150, 40)
        button.setStyleSheet(self.button_style())

        if on_click:
            button.clicked.connect(on_click)

        self.layout.addWidget(button, alignment=Qt.AlignCenter)

    def submit_items(self):
        items = self.item_input.toPlainText().splitlines()
        if items:
            self.show_message('Success', 'Items submitted successfully!')
        else:
            self.show_message('Error', 'No items entered.')

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
