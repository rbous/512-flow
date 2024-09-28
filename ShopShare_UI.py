
import sys
from PyQt5.QtWidgets import QApplication
from ui_func import SignInWindow


def main():
    app = QApplication(sys.argv)

    # Create an instance of the SignInWindow
    sign_in_window = SignInWindow()
    sign_in_window.show()

    # Start the application's event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

