#type_window.py
from PyQt5.QtWidgets import QWidget, QLabel,QVBoxLayout, QApplication, QTextEdit, QPlainTextEdit, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
import sys
import os
from core.chat_client import send 

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
        self.reply_area.setPlainText("")
        self.reply_area.setReadOnly(True)
        self.reply_area.setFixedSize(540,250)
        self.reply_area.setStyleSheet("""
            background-color: transparent;
            border: none;
            font-family: '微軟正黑體 Light';
            font-size:16px;
            font-color: (0,0,0,150);
            line-height: 150%;
        """)
        self.reply_area.setGeometry(26,78,550,73)

        #input box
        self.input_box = QTextEdit(self)
        self.input_box.setPlaceholderText("")
        self.input_box.setFixedSize(550,73)
        self.input_box.setStyleSheet("""
            QTextEdit{
                background-color: transparent;
                border: none;
                font-family: 'Comic Sans MS';
                font-size: 15px;
            }
        """)
        self.input_box.setGeometry(23,353,550,73)

        #send button
        self.send_button = QPushButton("Send", self)
        self.send_button.setFixedSize(60,30)
        '''
        self.send_button.setStyleSheet("""
            border-radius: 5px;
            border-color: purple;
            color: purple;
            background-color: rgba(190, 160, 206, 206)
            font-family: 'Comic Sans MS';
            font-weight: bold;
        """)
        '''
        self.send_button.move(510,390)
        self.send_button.clicked.connect(self.handle_send)

        #save chat history
        self.history = []


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

    def handle_send(self):
        user_text = self.input_box.toPlainText().strip()
        if not user_text:
            return

        user_html = f"""
            <div style = "margin-bottom:10px; font-family:'微軟正黑體 Light', 'Comic Sans MS'; font-size:15px; line-height: 1.3;">
                <b>芍芍:<b> <span>{user_text}<\span>
            <div>
        """

        self.reply_area.appendHtml(user_html)
        self.history.append(("user", user_text))

        try:
            response  = send(user_text, self.history, profile_id = "Elfie")
            elfie_html = f"""
            <div style= "margin-bottom: 15px; font-family:'微軟正黑體 Light', 'Comic Sans MS'; font-size:15px; line-height: 1.3;">
                <b>精靈:</b> <span>{response}<\span>
            <div>
            """
            self.reply_area.appendHtml(elfie_html)

        except Exception as e:
            self.reply_area.appendPlainText(f"[Error] {e}")

        self.input_box.clear()


if  __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = TypeWindow()
    window.show()
    sys.exit(app.exec_())
