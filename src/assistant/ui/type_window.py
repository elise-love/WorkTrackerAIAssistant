from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
import os

class TypeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600,400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        #load background img
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, "components", "type_window_1.jpg")
        self.pixmap = QPixmap(img_path)

        #background Qlabel
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True) #automaically scale to fit
        self.update_background()

      
        label = QLabel(" ", self)
        label.setAlignment(Qt.AlignCenter)

        #layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)

    def update_background(self):
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.resize(self.size())
        else:
            print(f"❌ 圖片載入失敗：{self.img_path}")