import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShopShare")
        self.setGeometry(100, 100, 1000, 900)
        self.setWindowIcon(QIcon("icon.png"))
        self.initUI()


    def initUI(self):

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)


        label = QLabel("Welcome",self)
        label.setFont(QFont("Arial", 20))
        label.setGeometry(0,0,500,100)
        label.setStyleSheet("color: purple;")
        label.setAlignment(Qt.AlignVCenter)

        back_ground = QLabel(self)
        back_ground.setGeometry(0, 0, 250, 250)

        pixmap = QPixmap("bg_gui.jpg")
        back_ground.setPixmap(pixmap)
        back_ground.setScaledContents(True)

        back_ground.setAlignment(Qt.AlignCenter)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()