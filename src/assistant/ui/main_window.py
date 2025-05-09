﻿#main_window.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize,Qt,QPoint
from PyQt5.QtGui import QPixmap #圖片資料
import sys
import os

from assistant.core.chat_client import send

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

        self.color_block = color_block

        self.minimized = False

        #settings for dragging
        self.mouse_is_dragging=False
        self.mouse_drag_position = QPoint() #表示一個 2D 點，初始為 (0, 0)

        #add Qlabel for icon
        self.icon_label = ClickableLabel(self)
        self.icon_label.setGeometry(10, 10, 200, 200) #(x, y, width, height(container))

        #add icon root to Pixamp
        icon_path = os.path.join(os.path.dirname(__file__),"components","elfie_icon_1.png")
        pixmap=QPixmap(icon_path)
        
        #add .scaled() method to Pixamp
        scaled_pixmap = pixmap.scaled(100,100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled_pixmap)

        #add input text box
        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(50,600,300,30)

        #send button
        self.send_button = QPushButton("Send",self)
        self.send_button.setGeometry(360,600,80,30)

        #function connect after clicking send button
        self.send_button.clicked.connect(self.send_text)

        #record chat history
        self.history=[]

        #chat box area
        self.chat_display = QTextEdit(self)
        self.chat_display.setGeometry(50, 350 ,390, 230)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            background-color: rgba(255, 255, 255,0.4);
            border-radius: 10px;
            padding: 5px;
        """)
   

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

    def mouseReleaseEvent(self,e):
        self.mouse_is_dragging = False

    def toggle_block(self):
         if self.minimized:
            self.setFixedSize(500, 700)
            self.color_block.setFixedSize(500, 700)
            self.color_block.show()

         else:
             self.setFixedSize(200,200)
             self.color_block.hide()
             self.icon_label.move(10,10)
         self.minimized = not self.minimized

    #input text and send
    def send_text(self):
        user_text = self.text_input.text().strip()
        if not user_text:
            return

        #input text
        print("User Input:",user_text)
        self.chat_display.append(f"<b>Me:</b>{user_text}") #<b>:bold
        self.history.append(("user",user_text))

        #call backend function send() to send user input
        try:
            reply = send(user_text, self.history)
        except Exception as e:
            self.chat_display.append(f"<b>Elfie:</b> Error: {e}")
            print("Error from backend:", e)
            return

        #display reply
        print("Elfie:",reply)
        self.chat_display.append(f"<b>Elife:</b> {reply}")
        self.history.append(("assistant", reply))

        #clear input text box
        self.text_input.clear()




class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseDoubleClickEvent(self,event):
        if self.parent():
            self.parent().toggle_block()

app = QApplication(sys.argv)

window= MainWindow()
window.show() 

app.exec()

