import sys
import random
import time
import math
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QTransform 


class DesktopPet(QWidget):
    """模仿 Shimeji 的桌面 PNG 寵物。"""

    SIZE        = 120   
    FPS         = 60
    WALK_SPEED  = 2            
    RUN_SPEED   = 5
    JUMP_SPEED  = 10     
    GRAVITY     = 0.6

    def __init__(self):
        super().__init__()

        # 視窗外觀
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        #載入圖片
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, "anime_girl.png")
        self.image = QPixmap(img_path)

        # 取得螢幕可用範圍
        self.screen_rect = QApplication.primaryScreen().availableGeometry()

        #運動狀態
        self.xv = 0
        self.yv = 0
        self.on_ground = False
        self.facing = 1

        self.state = "idle"
        self.state_until = time.time() + self._rand_dur("idle")
        self._choose_new_target()            # 目標點 (tx, ty)

        #timer
        self.timer = QTimer(self, timeout=self.tick)
        self.timer.start(int(1000 / self.FPS))

        # 初始位置
        self.move(
            random.randint(0, self.screen_rect.width()  - self.SIZE),
            random.randint(0, self.screen_rect.height() - self.SIZE),
        )
        self.show()

    #state
    def _rand_dur(self, s):
        table = {
            "idle": random.uniform(1.5, 3),
            "walk": random.uniform(2, 4),
            "run":  random.uniform(1.5, 3),
            "jump": 0.6,
        }
        return table.get(s, 1)

    def _choose_new_target(self):
        pad = 10  # 不要貼邊選
        self.tx = random.randint(pad, self.screen_rect.width()  - self.SIZE - pad)
        self.ty = random.randint(pad, self.screen_rect.height() - self.SIZE - pad)

    def _enter_state(self, new_state):
        self.state = new_state
        self.state_until = time.time() + self._rand_dur(new_state)

        if new_state == "idle":
            self.xv = self.yv = 0

        elif new_state in ("walk", "run"):
            self._choose_new_target()
            speed = self.WALK_SPEED if new_state == "walk" else self.RUN_SPEED
            angle = math.atan2(self.ty - self.y(), self.tx - self.x())
            self.xv = speed * math.cos(angle)
            self.yv = speed * math.sin(angle)
            self.facing = 1 if self.xv >= 0 else -1

        elif new_state == "jump":
            # 小跳一下：保持原本水平速度，給向上速度
            self.yv = -self.JUMP_SPEED
            self.on_ground = False

    def _next_state(self):
        return random.choice(
            ["idle"] * 2 + ["walk"] * 3 + ["run"] * 2 + ["jump"]
        )

    #
    def tick(self):
        now = time.time()
        # 狀態到期 → 換下一個隨機狀態
        if now >= self.state_until:
            self._enter_state(self._next_state())

        # 移動 & 重力
        if self.state in ("walk", "run"):
            # 到達目標改成 idle
            if (abs(self.x() - self.tx) < abs(self.xv) * 2 and
                    abs(self.y() - self.ty) < abs(self.yv) * 2):
                self._enter_state("idle")

        if not self.on_ground:
            self.yv += self.GRAVITY  # 重力只在空中作用

        # 計算下一位置
        nx = self.x() + self.xv
        ny = self.y() + self.yv

        #border 反彈
        if nx < 0:
            nx = 0
            self.xv = abs(self.xv)
            self.facing = 1
        elif nx + self.SIZE > self.screen_rect.width():
            nx = self.screen_rect.width() - self.SIZE
            self.xv = -abs(self.xv)
            self.facing = -1

        if ny < 0:
            ny = 0
            self.yv = 0
        elif ny + self.SIZE > self.screen_rect.height():
            ny = self.screen_rect.height() - self.SIZE
            self.yv = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # 實際移動
        self.move(int(nx), int(ny))
        self.update()

    #paint
    def paintEvent(self, _evt):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), Qt.transparent)

        if self.image.isNull():
            return

        if self.facing == -1:                       # 向左 → 水平翻轉
            flip = QTransform().scale(-1, 1)        # 建立翻轉矩陣
            flipped_pix = self.image.transformed(flip, Qt.SmoothTransformation)
            p.drawPixmap(0, 0, self.SIZE, self.SIZE, flipped_pix)
        else:                                       # 向右 → 原圖
            p.drawPixmap(0, 0, self.SIZE, self.SIZE, self.image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec_()) 