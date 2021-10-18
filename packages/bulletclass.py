"""
@version:
@author: DQ
@time: 2021-10-13
@file: bulletclass.py
@function: 
@modify: 2021-10-18修改update函数，修复子弹可同时判定的bug
"""

import pygame

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

WIN_SIZE = (640, 480)
SPEED = 5  # 一次移动5像素


class OneBullet():
    pos = None  # 位置坐标
    ori = None  # 方向

    def __init__(self, coord, c_ori):
        self.pos = [coord[0], coord[1]]
        self.ori = c_ori

    def move(self, bullet_size):
        if self.ori == UP:
            self.pos[1] -= SPEED
        elif self.ori == DOWN:
            self.pos[1] += SPEED
        elif self.ori == LEFT:
            self.pos[0] -= SPEED
        elif self.ori == RIGHT:
            self.pos[0] += SPEED

        if self.pos[0] < 0 or self.pos[0] >= WIN_SIZE[0] - bullet_size[0] or \
                self.pos[1] < 0 or self.pos[1] >= WIN_SIZE[1] - bullet_size[1]:
            return False
        else:
            return True

    def check_hit_bricks(self, bullet_size, bricks):
        for i in bricks.brickslist:
            if i.pos[0] - bullet_size[0] < self.pos[0] < i.pos[0] + bricks.brick_size[0] and \
                    i.pos[1] - bullet_size[1] < self.pos[1] < i.pos[1] + bricks.brick_size[1]:
                if i.remain_HP > 0:
                    i.remain_HP -= 1
                return True
        return False

    def check_hit_tank(self, bullet_size, tank):
        if tank.tank_pos[0] - bullet_size[0] < self.pos[0] < tank.tank_pos[0] + tank.tank_size[0] and \
                tank.tank_pos[1] - bullet_size[1] < self.pos[1] < tank.tank_pos[1] + tank.tank_size[1]:
            tank.get_shot()
            return True
        return False


class Bullets():
    __obj = None  # 单态
    bullet_img = None
    bullet_size = None
    bulletslist = None  # 存储子弹对象的列表

    def __new__(cls, *args, **kwargs):
        if not cls.__obj:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self, filename):
        """
        初始化，传入子弹素材
        """
        self.bullet_img = pygame.image.load(filename)
        self.bullet_size = self.bullet_img.get_size()
        self.bulletslist = []

    def add_bullet(self, b_obj):
        self.bulletslist.append(b_obj)

    def __draw(self, window):
        for i in self.bulletslist:
            window.blit(self.bullet_img, i.pos)

    def __wipe(self, window):
        for i in self.bulletslist:
            pygame.draw.rect(window, (0, 0, 0),
                             (i.pos[0], i.pos[1],
                              self.bullet_size[0], self.bullet_size[1]))

    def update(self, window, bricks, tank_player, tanks_ai):
        self.__wipe(window)
        for i in self.bulletslist:
            if not i.move(self.bullet_size):
                self.bulletslist.remove(i)

            elif i.check_hit_bricks(self.bullet_size, bricks):
                self.bulletslist.remove(i)

            elif i.check_hit_tank(self.bullet_size, tank_player):
                self.bulletslist.remove(i)

            else:
                for tk in tanks_ai:
                    if i.check_hit_tank(self.bullet_size, tk):
                        self.bulletslist.remove(i)
                        break

        self.__draw(window)
