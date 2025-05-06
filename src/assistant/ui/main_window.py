from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize,Qt,QPoint
from PyQt5.QtGui import QPixmap #圖片資料
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #window settings
        self.setFixedSize(500,700)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCentralWidget(QWidget()) #base widget

        #color block settings
        color_block = QWidget(self)
        color_block.setFixedSize(500,700)
        #color_block.setGeometry(50 ,100, 300 ,400)
        color_block.setStyleSheet("""
            background-color: rgba(202, 192, 237, 206);
            border-radius: 20px;
        """)

        #settings for dragging
        self.is_dragging=False
        self._drag_position = QPoint() #表示一個 2D 點，初始為 (0, 0)

        #add Qlabel for icon
        self.label = QLabel(self) #QLabel(self) 表示這個 label 是屬於 MainWindow 視窗內的
        self.label.setGeometry(335, 25, 200, 200) #(x, y, width, height(container))

        #add icon
        icon_path = os.path.join(os.path.dirname(__file__),"components","elfie_icon_1.png")
        pixmap=QPixmap(icon_path)
        scaled_pixmap = pixmap.scaled(100,100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        

    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton:
            self.is_dragging = True
            self._drag_position = e.globalPos() - self.frameGeometry().topLeft()
            #e.globalPos()：回傳滑鼠在 螢幕上 的座標位置

            e.accept()

    def mouseMoveEvent(self, e):
        if self.is_dragging and e.buttons() & Qt.LeftButton:
            self.move(e.globalPos() - self._drag_position)
            e.accept()
        """
        event.buttons() & Qt.LeftButton:
            使用位元運算 & 來檢查 左鍵是否包含在目前被按的按鍵中。
            如果有按下左鍵，就會是 True，否則是 False。
        """

    def mouseReleaseEvent(self,e):
        self.is_dragging = False

app = QApplication(sys.argv)

window= MainWindow()
window.show() 

app.exec()

