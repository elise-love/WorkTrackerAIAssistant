﻿#main_window.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui import QPixmap 
import sys
import os
from ui.type_window import TypeWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #window settings
        self.setFixedSize(1500,1400)
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
            padding: 0;
        """)

        self.color_block = color_block

        self.minimized = False

        #settings for dragging
        self.mouse_is_dragging=False
        self.mouse_drag_position = QPoint() #表示一個 2D 點，初始為 (0, 0)

        #add Qlabel for icon
        self.icon_label = ClickableLabel(self, double_click_callback=self.toggle_block)
        self.icon_label.setGeometry(5, 0, 200, 200) #(x, y, width, height(container))

        #add icon root to Pixamp
        icon_path = os.path.join(os.path.dirname(__file__),"components","elfie_icon_1.png")
        pixmap=QPixmap(icon_path)
        
        #add .scaled() method to Pixamp
        scaled_pixmap = pixmap.scaled(100,100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled_pixmap)

        #type-icon setup
        self.type_window = TypeWindow()
        self.type_window_display = False
        self.type_icon = ClickableLabel(self, double_click_callback = self.toggle_typeWindow)
        self.type_icon.setGeometry(215, 600,  100, 100)

        type_icon_path = os.path.join(os.path.dirname(__file__),"components","type-icon.png")
        type_pixmap = QPixmap(type_icon_path)
        scaled_type_pixmap = type_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.type_icon.setPixmap(scaled_type_pixmap)

        #plan_display area
        self.plan_display_area = QPlainTextEdit(self)
        self.plan_display_area.setPlainText("")
        self.plan_display_area.setReadOnly(True)
        self.plan_display_area.setFixedSize(480,450)
        self.plan_display_area.setStyleSheet("""
            border: none;
            border-radius: 10px;
            background-color: transparent;
        """)
        self.plan_display_area.move(11,160)

        self.move(1420,380)


    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton:
            self.mouse_is_dragging = True
            self.mouse_drag_position = e.globalPos() - self.frameGeometry().topLeft()
            #e.globalPos()：回傳滑鼠在 螢幕上 的座標位置

            e.accept()

    def mouseMoveEvent(self, e):
        if self.mouse_is_dragging and (e.buttons() & Qt.LeftButton):
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


    def toggle_typeWindow(self):
        if not self.type_window_display:
            self.type_window.show()

        else:
            self.type_window.hide()
        self.type_window_display = not self.type_window_display


class ClickableLabel(QLabel):
    def __init__(self, parent=None, single_click_callback=None, double_click_callback=None):
        super().__init__(parent)
        self.single_click_callback = single_click_callback
        self.double_click_callback = double_click_callback

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.single_click_callback:
            self.single_click_callback()

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton and self.double_click_callback:
            self.double_click_callback()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window= MainWindow()
    window.show() 
    app.exec()