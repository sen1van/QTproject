import sys
from random import randint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel
from PyQt5.QtCore import *


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pressD = False
        self.pressA = False
        self.setGeometry(700, 100, 600, 900)
        self.setWindowTitle('doodle jump')

        self.GRAVITY = 0.02
        self.SPEED = 1
        self.COLLISION_HEIGHT = 10
        # Игрок, вообще тут и дебаг, но мне пофих на коменты
        self.player = QLabel(self)
        self.player.collision_offset = [35, 80]
        self.player.collision_width = 60
        self.player.sprite_size = [100, 90]
        self.player.velocity = [0, 0]
        self.player.position = [225, 400]
        self.player.setPixmap(QPixmap("player.png"))
        self.player.setScaledContents(True)
        self.player.resize(
            self.player.sprite_size[0], self.player.sprite_size[1])

        self.degub_collision = QLabel(self)
        self.degub_collision.setPixmap(QPixmap("debug_collision.png"))
        self.degub_collision.setScaledContents(True)
        self.degub_collision.resize(
            self.player.collision_width, self.COLLISION_HEIGHT)
        self.degub_collision.move(
            self.player.collision_offset[0], self.player.collision_offset[1])

        # платформы
        self.platforms = []
        for i in range(10):
            self.platforms += [QLabel(self)]
            self.platforms[i].setPixmap(QPixmap("default_platform.png"))
            self.platforms[i].setScaledContents(True)
            self.platforms[i].size = [100, 30]
            self.platforms[i].id = i
            self.platforms[i].resize(
                self.platforms[i].size[0],  self.platforms[i].size[1])
            self.platforms[i].move(randint(0, 500), i * 90)
            self.platforms[i].y_position = self.platforms[i].y()

        # найстройки игры
        self.game_speed = 1
        # таймер, он тут (1000 / 6) кадров в сек
        self.runner_timer = QTimer()
        self.runner_timer.timeout.connect(self.run)
        self.runner_timer.start(6)

    def run(self):
        for platform in self.platforms:

            if (self.player.collision_width/2 + platform.size[0]/2) * -1 < ((platform.x() + (platform.size[0]/2)) - ((self.player.x() + self.player.collision_offset[0]) + (self.player.collision_width/2))) < (self.player.collision_width/2 + platform.size[0]/2):
                if platform.y() + (platform.size[1]/2) > (self.player.y() + self.player.collision_offset[1] + self.COLLISION_HEIGHT) > platform.y():
                    if self.player.velocity[1] > 0.1:
                        self.player.velocity[1] = -3
            if self.player.position[1] <= 400 and self.player.velocity[1] < 0:
                platform.y_position -= self.player.velocity[1]
                platform.move(platform.x(), int(platform.y_position))
            if platform.y() > 900:
                platform.y_position = -30
                platform.move(randint(0, 500), platform.y_position)
        if self.player.position[1] <= 400:
            self.player.position[1] = 400
        self.player.velocity[1] += self.GRAVITY

        self.player.position[0] += self.player.velocity[0]
        self.player.position[1] += self.player.velocity[1]
        self.degub_collision.move(
            int(self.player.position[0] + self.player.collision_offset[0]), int(self.player.position[1] + self.player.collision_offset[1]))
        self.player.move(int(self.player.position[0]), int(
            self.player.position[1]))

    def mouseMoveEvent(self, event):
        self.player.position[0] =  event.x(
        ) - self.player.collision_width/2 - self.player.collision_offset[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Example2()
    ex1.show()
    sys.exit(app.exec())
