import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtGui import QPainter, QColor, QBrush


class BouncingOval(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(150, 100) 

        # Movement setup

        #movement speed (how many pixels per frame))
        #moves the oval a bit every 30ms
        self.dx = 5 
        self.dy = 5

        #Timer: updates oval's position every 30ms
        self.timer = QTimer() 
        self.timer.timeout.connect(self.move_oval) #call move_oval() every 30ms
        self.timer.start(30)

        #Color setup
        self.current_color = QColor(180, 130, 255, 200)
        self.target_color = self.random_color()
        self.color_change_start_time = QTime.currentTime()
        self.start_color = self.current_color
        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.update_color_target)
        self.color_timer.start(2000) 

        #initial position
        self.move(100, 100)
        self.show()


    def random_color(self):
        return QColor(
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
            200 #Alpha is fixed to 150 for consistent transparency
            )

    def update_color_target(self):
        self.color_change_start_time = QTime.currentTime() #transits new color
        self.start_color = self.current_color #record currnt color
        self.target_color = self.random_color() #generate new color

    def interpolate_color(self):
        #caculate elapsed tume since transiton started
        elapsed = self.color_change_start_time.msecsTo(QTime.currentTime())
        
        t = min(elapsed / 2000.0, 1.0)  # normalized [0,1]

        # Define linear interpolation´¡´Ó function\
        #smooth transition wach RGBA component of the color
        def lerp(a, b): return a + (b - a) * t

        r = int(lerp(self.start_color.red(), self.target_color.red()))
        g = int(lerp(self.start_color.green(), self.target_color.green()))
        b = int(lerp(self.start_color.blue(), self.target_color.blue()))
        a = int(lerp(self.start_color.alpha(), self.target_color.alpha()))

        self.current_color = QColor(r, g, b, a)
        self.update()


    def paintEvent(self, event):

        #updat current color by interpolating toward the target
        self.interpolate_color()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) #smooth edge algorithm
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(Qt.NoPen) #no border
        painter.drawEllipse(0, 0, self.width(), self.height())

    def move_oval(self):
        screen_rect = QApplication.desktop().screenGeometry() #screen size
        
        #calculate new position
        x = self.x() + self.dx
        y = self.y() + self.dy

        #collision check
        if x <= 0 or x + self.width() >= screen_rect.width():
            self.dx *= -1 #reverse horizontal direction

        if y <= 0 or y + self.height() >= screen_rect.height():
            self.dy *= -1

        self.move(self.x() + self.dx, self.y() + self.dy)



def start_bouncing_oval():
    app = QApplication(sys.argv)
    oval = BouncingOval()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_bouncing_oval()
