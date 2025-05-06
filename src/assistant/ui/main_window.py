from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize,Qt,QPoint
from PyQt5.QtGui import QPixmap #圖片資料
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #initial window settings
        self.full_size = QSize(500,700)
        self.icon_size = QSize(200,200)
        self.minimize_block = False

        self.setFixedSize(self.full_size)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCentralWidget(QWidget()) #base widget

        #color block settings
        self.color_block = QWidget(self)
        self.color_block.setFixedSize(self.full_size)
        #color_block.setGeometry(50 ,100, 300 ,400)
        self.color_block.setStyleSheet("""
            background-color: rgba(202, 192, 237, 206);
            border-radius: 20px;
        """)

        #settings for dragging
        self.mouse_is_dragging=False
        self.mouse_drag_position = QPoint() #表示一個 2D 點，初始為 (0, 0)

        #add Qlabel for icon
        self.icon_label = QLabel(self) #QLabel(self) 表示這個 label 是屬於 MainWindow 視窗內的
        self.icon_label.setGeometry(335, 25, 200, 200) #(x, y, width, height(container))

        #add icon root to Pixamp
        icon_path = os.path.join(os.path.dirname(__file__),"components","elfie_icon_1.png")
        pixmap=QPixmap(icon_path)
        
        #add .scaled() method to Pixamp
        scaled_pixmap = pixmap.scaled(100,100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled_pixmap)
        
        #icon click settings (only when block minimized)
        self.icon_label.mousePressEvent = self.icon_mouse_press
        self.icon_label.mouseMoveEvent = self.icon_mouse_move
        self.icon_label.mouseReleaseEvent = self.icon_mouse_release

    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton:
            self.mouse_is_dragging = True
            self.mouse_drag_position = e.globalPos() - self.frameGeometry().topLeft()
            #e.globalPos()：回傳滑鼠在 螢幕上 的座標位置

            e.accept()

    def mouseMoveEvent(self, e):
        if self.mouse_is_dragging and e.buttons() & Qt.LeftButton:
            self.move(e.globalPos() - self.mouse_drag_position)
            e.accept()
        else:
            #minimize block
            self.setFixedSize(self.icon_size)
            self.color_block.hide()
            self.icon_label.move(10,10)
            self.minimize_block = True
        e.accept()

    def mouseReleaseEvent(self,e):
        self.mouse_is_dragging = False

    #icon dragging methods
    def icon_mouse_press(self, e):
        if e.button() == Qt.LeftButton:
            if self.minimize_block:
                # minimize and drag
                self.mouse_is_dragging = True
                self.mouse_drag_position = e.globalPos() - self.frameGeometry().topLeft()
            else:
                # enlarge
                self.setFixedSize(self.icon_size)
                self.color_block.hide()
                self.icon_label.move(10, 10)
                self.minimize_block = True
            self.minimize_block = not self.minimize_block

    def icon_mouse_move(self,e):
        if self.mouse_is_dragging and e.buttons()&Qt.LeftButton:
            self.move(e.globalPos()-self.mouse_drag_position)
            e.accept()
    def icon_mouse_release(self,e):
         self.mouse_is_dragging = False

app = QApplication(sys.argv)

window= MainWindow()
window.show()
app.exec()