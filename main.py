import sys
from random import randint
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

from playsound import playsound

from collision import *


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 100, 600, 900)
        self.setWindowTitle('doodle jump')
        self.backgrounds = []
        for i in range(3):
            self.backgrounds += [QLabel(self)]
            self.backgrounds[i].setPixmap(
                QPixmap("textures/background/background.png"))
            self.backgrounds[i].move(0, i * (-1800))
            self.backgrounds[i].y_position = i * (-900-450)

        # джамп пад
        self.jump_pad_in_game = False

        self.jump_pad = QLabel(self)
        self.jump_pad.setPixmap(QPixmap("textures/power_ups/jump_pad"))
        self.jump_pad.setScaledContents(True)
        self.jump_pad.resize(
            35, 15)
        self.jump_pad.move(
            -300, -300)

        # self.rocket.move(
        #     -300, -300)
        # платформы
        self.break_platform = QPixmap("textures/platforms/break_platform")
        self.default_platform = QPixmap(
            "textures/platforms/default_platform")
        self.secret_platform = QPixmap(
            "textures/platforms/secret_platform.png")
        self.platforms = []
        for i in range(10):
            self.platforms += [QLabel(self)]
            self.platforms[i].setPixmap(self.default_platform)
            self.platforms[i].setScaledContents(True)
            self.platforms[i].size = [100, 30]
            self.platforms[i].id = i
            self.platforms[i].has_rocket = False
            self.platforms[i].has_jump_pad = False
            self.platforms[i].breakable = False
            self.platforms[i].is_break = False
            self.platforms[i].resize(
                self.platforms[i].size[0],  self.platforms[i].size[1])
            self.platforms[i].move(randint(0, 500), i * 90)
            self.platforms[i].y_position = self.platforms[i].y()

        # Игрок, вообще тут и дебаг, но мне пофих на коменты
        self.last_player_pos = 0
        self.GRAVITY = 0.02
        self.SPEED = 1
        self.player = QLabel(self)
        self.player_normal = QPixmap("textures/player/player.png")
        self.player_mirror = QPixmap("textures/player/player_mirror.png")

        self.player_normal_secret = QPixmap(
            "textures/player/secret/secret_player.png")
        self.player_mirror_secret = QPixmap(
            "textures/player/secret/secret_player_mirror.png")

        self.player.collision_offset = [30, 80]
        self.player.mirrored = False
        self.player.collision_size = [55, 10]
        self.player.sprite_size = [120, 90]
        self.player.velocity = [0, 0]
        self.player.position = [225, 400]
        self.player.move(self.player.position[0], self.player.position[1])
        self.player.setPixmap(self.player_normal)
        self.player.setScaledContents(True)
        self.player.resize(
            self.player.sprite_size[0], self.player.sprite_size[1])

        self.degub_collision = QLabel(self)
        self.degub_collision.setPixmap(
            QPixmap("textures/debug_collision.png"))
        self.degub_collision.setScaledContents(True)
        self.degub_collision.resize(
            self.player.collision_size[0], self.player.collision_size[1])
        self.degub_collision.move(
            self.player.collision_offset[0], self.player.collision_offset[1])

        # rocket
        self.rocket = QLabel(self)
        self.rocket.setPixmap(QPixmap("textures/power_ups/rocket.png"))
        self.rocket.setScaledContents(True)
        self.rocket.resize(
            25, self.player.sprite_size[1])
        self.rocket.move(-300, -300)

        self.rocket_in_game = False
        # найстройки игры
        self.JUMP_POWER = -3.4
        self.game_speed = 1
        self.secret_avaible = False
        self.is_game_end = True

        # интерфейс проигрыша
        self.start_button = QPushButton("", self)
        self.start_button.resize(300, 150)
        self.start_button.setFlat(True)
        self.start_button.setIcon(QIcon('textures/ui/play_button.png'))
        self.start_button.setIconSize(QSize(300, 150))
        self.start_button.clicked.connect(self.game_start)

        self.game_title = QLabel(self)
        self.game_title.setPixmap(QPixmap("textures/ui/doodle_jump_python"))
        self.game_title.resize(500, 200)
        self.game_title.move(50, 100)
        self.game_title.setScaledContents(True)

        self.font_score = QFont()
        self.font_score.setFamily("Comic Sans MS")
        self.font_score.setPointSize(23)

        self.score = QLabel("Счет: 0", self)
        self.score.setFont(self.font_score)
        self.score.score = 0
        self.score.resize(10000000, 46)
        self.score.move(20, 20)

        self.secret_button = QPushButton("", self)
        self.secret_button.resize(10, 10)
        self.secret_button.setFlat(True)
        self.secret_button.clicked.connect(self.game_start_secret)
        # таймер, он тут (1000 / 6) кадров в сек
        self.runner_timer = QTimer()
        self.runner_timer.timeout.connect(self.run)
        self.runner_timer.start(6)

    def run(self):
        if not self.is_game_end:
            collision_pos = [self.player.position[0] + self.player.collision_offset[0],
                             self.player.position[1] + self.player.collision_offset[1]]
            for platform in self.platforms:
                if self.player.velocity[1] > 0.1 and not platform.is_break:
                    if collide_2_rect([platform.x(), platform.y_position], platform.size, collision_pos, self.player.collision_size):
                        print(platform.x(), platform.y())
                        print(*self.player.position)

                        if platform.breakable and randint(1, 3) == 1:
                            playsound(
                                'sounds/jump_breakable/break.wav', False)
                        else:
                            self.player.velocity[1] = self.JUMP_POWER
                            if platform.has_jump_pad:
                                if collide_2_lines(platform.x()+15, platform.size[0]-30, collision_pos[0], self.player.collision_size[0]):
                                    self.player.velocity[1] = self.JUMP_POWER * 2
                                    playsound(
                                        f'sounds/power_ups/jump_pad.wav', False)
                                else:
                                    playsound(
                                        f'sounds/jump_default/jump{randint(1,2)}.wav', False)
                            elif platform.has_rocket:
                                if collide_2_lines(platform.x()+15, platform.size[0]-30, collision_pos[0], self.player.collision_size[0]):
                                    self.player.velocity[1] = self.JUMP_POWER * 6
                                    platform.has_rocket = False
                                    self.rocket_in_game = False
                                    self.rocket.move(-300, -300)
                                    playsound(
                                        'sounds/power_ups/rocket.wav', False)
                                else:
                                    playsound(
                                        f'sounds/jump_default/jump{randint(1,2)}.wav', False)
                            elif platform.breakable:
                                playsound(
                                    'sounds/jump_breakable/not_break.wav', False)
                            else:
                                if self.secret_avaible:
                                    playsound(
                                        f'sounds/jump_default/secret_jump.wav', False)
                                else:
                                    playsound(
                                        f'sounds/jump_default/jump{randint(1,2)}.wav', False)

                        if platform.breakable:
                            platform.is_break = True
                            platform.hide()

                if self.player.position[1] <= 400 and self.player.velocity[1] < 0:
                    platform.y_position -= self.player.velocity[1]
                    if platform.has_jump_pad and self.jump_pad_in_game:
                        self.jump_pad.move(
                            int(platform.x() + platform.size[0]/2 - 15), int(platform.y_position)-13)
                    if platform.has_rocket and self.rocket_in_game:
                        self.rocket.move(
                            int(platform.x() + platform.size[0]/2 - 16), int(platform.y_position)-self.player.sprite_size[1])
                    platform.move(platform.x(), int(platform.y_position))
                if platform.y() > 900:
                    self.score.score += 1
                    self.score.setText("Счёт: " + str(self.score.score))
                    platform.is_break = False
                    platform.y_position = -30 + randint(-1, 1)
                    platform.breakable = (randint(0, 3) == 0)

                    if platform.has_rocket and self.rocket_in_game:
                        self.rocket_in_game = False
                        platform.has_rocket = False
                        self.rocket.move(-300, -300)
                    elif not self.rocket_in_game and not platform.breakable:
                        if randint(1, 30) == 1:
                            self.rocket_in_game = True
                            platform.has_rocket = True

                    if platform.has_jump_pad and self.jump_pad_in_game:
                        self.jump_pad_in_game = False
                        platform.has_jump_pad = False
                        self.jump_pad.move(-300, -300)
                    elif not self.jump_pad_in_game and not platform.breakable and not platform.has_rocket:
                        if randint(1, 6) == 1:
                            self.jump_pad_in_game = True
                            platform.has_jump_pad = True

                    if platform.breakable:
                        platform.setPixmap(self.break_platform)
                        platform.show()
                    else:
                        platform.setPixmap(self.default_platform)
                        platform.show()
                        if self.secret_avaible and randint(1, 3) == 1:
                            platform.setPixmap(self.secret_platform)
                    platform.move(randint(0, 500), platform.y_position)
            for background in self.backgrounds:
                if self.player.position[1] <= 400 and self.player.velocity[1] < 0:
                    background.y_position -= self.player.velocity[1]
                    background.move(background.x(), int(background.y_position))
                if background.y_position >= 900:
                    background.y_position -= (900 + 450) * 3

            if self.player.position[1] <= 400:
                self.player.position[1] = 400
            self.player.velocity[1] += self.GRAVITY

            self.player.position[0] += self.player.velocity[0]
            self.player.position[1] += self.player.velocity[1]
            if self.player.velocity[1] < self.JUMP_POWER * 2 - 1:
                if self.player.mirrored:
                    self.rocket.move(
                        int(self.player.position[0] + 5), int(self.player.position[1]))
                else:
                    self.rocket.move(int(
                        self.player.position[0]+self.player.sprite_size[0]-30), int(self.player.position[1]))
            elif not self.rocket_in_game:
                self.rocket.move(-300, -300)
            if self.player.position[1] > 900:
                self.is_game_end = True

            self.degub_collision.move(
                int(self.player.position[0] + self.player.collision_offset[0]), int(self.player.position[1] + self.player.collision_offset[1]))
            self.player.move(int(self.player.position[0]), int(
                self.player.position[1]))
        else:
            self.game_end()

    def mouseMoveEvent(self, event):
        self.player.position[0] = event.x(
        ) - self.player.collision_size[0]/2 - self.player.collision_offset[0]
        if self.last_player_pos - self.player.position[0] > 1.8:
            if self.secret_avaible:
                self.player.setPixmap(self.player_normal_secret)
            else:
                self.player.setPixmap(self.player_normal)
            self.player.mirrored = False
            self.last_player_pos = self.player.position[0]
        elif self.last_player_pos - self.player.position[0] < -1.8:
            if self.secret_avaible:
                self.player.setPixmap(self.player_mirror_secret)
            else:
                self.player.setPixmap(self.player_mirror)
            self.player.mirrored = True
            self.last_player_pos = self.player.position[0]

    def game_start(self):
        self.jump_pad_in_game = False
        self.rocket_in_game
        self.secret_button.hide()
        self.secret_avaible = False
        self.is_game_end = False
        self.start_button.hide()
        self.game_title.hide()
        self.player.velocity = [0, 0]
        self.player.position = [225, 400]
        self.score.score = 0
        self.score.setText("Счёт: 0")
        for i in range(10):
            self.platforms[i].setPixmap(self.default_platform)
            self.platforms[i].has_rocket = False
            self.platforms[i].has_jump_pad = False
            self.platforms[i].breakable = False
            self.platforms[i].is_break = False
            self.platforms[i].move(randint(0, 500), i * 90)
            self.platforms[i].y_position = self.platforms[i].y()
            self.platforms[i].show()

    def game_end(self):
        self.game_title.show()
        for i in range(10):
            self.platforms[i].hide()
        self.jump_pad_in_game = False
        self.rocket_in_game = False
        self.rocket.move(-300, -300)
        self.jump_pad.move(-300, -300)
        self.player.move(225, 400)
        self.start_button.move(150, 580)
        self.start_button.show()

    def game_start_secret(self):
        self.secret_button.hide()
        self.secret_avaible = True
        self.is_game_end = False
        self.start_button.hide()
        self.game_title.hide()
        self.player.velocity = [0, 0]
        self.player.position = [225, 400]
        for i in range(10):
            self.platforms[i].setPixmap(self.default_platform)
            self.platforms[i].has_rocket = False
            self.platforms[i].has_jump_pad = False
            self.platforms[i].breakable = False
            self.platforms[i].is_break = False
            self.platforms[i].move(randint(0, 500), i * 90)
            self.platforms[i].y_position = self.platforms[i].y()
            self.platforms[i].show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Example2()
    ex1.show()
    sys.exit(app.exec())
