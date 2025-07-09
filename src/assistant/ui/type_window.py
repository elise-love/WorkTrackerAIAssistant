#type_window.py
from PyQt5.QtWidgets import QWidget, QLabel,QVBoxLayout, QApplication, QTextEdit, QPlainTextEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
import sys
import os

class TypeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600,450)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        #load background img
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, "components", "type_window.png")
        self.pixmap = QPixmap(img_path)

        #background Qlabel
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True) #automaically scale to fit
        self.background_label.setMouseTracking(True)
        self.background_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.update_background()

      
        label = QLabel(" ", self)
        label.setAlignment(Qt.AlignCenter)

        #layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.setContentsMargins(0, 0, 0, 0)

        #settings for dragging
        self.mouse_is_dragging = False
        self.mouse_drag_position = QPoint()
        self.setMouseTracking(True)

        #reply area
        self.reply_area = QPlainTextEdit(self)
        self.reply_area.setPlainText("A stalking wolf wants to eat the girl and the food in the basket. After he inquires as to where she is going, he suggests that she pick some flowers as a present for her grandmother. While she goes in search of flowers, he goes to the grandmother's house and gains entry by pretending to be Riding Hood. He swallows the grandmother whole, climbs into her bed, and waits for the girl, disguised as the grandmother.")
        self.reply_area.setReadOnly(True)
        self.reply_area.setFixedSize(540,250)
        self.reply_area.setStyleSheet("""
            background-color: transparent;
            border: none;
            font-family: '萌神手書體';
            font-size:16px;
            font-color: (0,0,0,150);
            line-height: 150%;
        """)
        self.reply_area.setGeometry(26,78,550,73)

        '''
        #assistant label
        assistant_lable = QLabel("小精靈: ", self)
        assistant_lable.setStyleSheet("""
            font-size: 17px;
            font-family: '萌神手書體';
            color: black;
        """)
        self.assistant_label = assistant_lable
        assistant_lable.setGeometry(30,73,50,20)
        '''

        #type area
        self.type_area = QTextEdit(self)
        self.type_area.setPlaceholderText("")
        self.type_area.setFixedSize(550,73)
        self.type_area.setStyleSheet("""
            QTextEdit{
                background-color: transparent;
                border: none;
                font-family: 'Comic Sans MS';
                font-size: 14px;
            }
        """)
        self.type_area.setGeometry(23,353,550,73)

        '''
        #user label
        user_lable = QLabel("芍芍: ", self)
        user_lable.setStyleSheet("""
            font-size: 15px;
            font-family: '萌神手書體';
            color: black;
        """)
        self.user_label = user_lable
        user_lable.setGeometry(30,355,35,20)
        '''

    def update_background(self):
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.resize(self.size())
            self.background_label.lower()

    def mousePressEvent(self,e):
        if e.button() == Qt.LeftButton:
            self.mouse_is_dragging = True
            self.mouse_drag_position = e.globalPos() - self.frameGeometry().topLeft()
            e.accept()
    
    def mouseMoveEvent(self ,e):
        if  self.mouse_is_dragging and (e.buttons() & Qt.LeftButton):
            self.move(e.globalPos() - self.mouse_drag_position)
            e.accept()

    def mouseReleaseEvent(self, e):
        self.mouse_is_dragging = False


if  __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = TypeWindow()
    window.show()
    sys.exit(app.exec_())
