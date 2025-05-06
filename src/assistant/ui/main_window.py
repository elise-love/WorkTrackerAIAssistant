from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize,Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400,600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCentralWidget(QWidget()) #base widget

        color_block = QWidget(self)
        color_block.setFixedSize(400,600)
        #color_block.setGeometry(50 ,100, 300 ,400)
        color_block.setStyleSheet("""
            background-color: rgba(225, 255, 255, 180);
            border-radius: 20px;
        """)

            




app = QApplication(sys.argv)

window= MainWindow()
window.show() 

app.exec()

