"""
@version:
@author: DQ
@time: 2021-10-13
@file: tankclass.py
@function: 
@modify: 
"""

import pygame
from . import bulletclass
from . import brickclass

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

WIN_SIZE = (640, 480)
SPEED = 2  # 一次移动2像素


class Tank():
    tank_img_up = None
    tank_img_down = None
    tank_img_left = None
    tank_img_right = None
    tank_pos = None  # 坦克左上角位置
    tank_state = None  # 上下左右四个状态
    tank_size = None  # 坦克像素尺寸
    __ifmove = None  # 是否持续移动
    __ifshot = None  # 是否被击毁
    __shotcount = None  # 击毁特效计数

    def __init__(self, tankfile):
        self.tank_img_up = pygame.image.load(tankfile)
        self.tank_img_down = pygame.transform.rotozoom(self.tank_img_up, 180, 1)
        self.tank_img_left = pygame.transform.rotozoom(self.tank_img_up, 90, 1)
        self.tank_img_right = pygame.transform.rotozoom(self.tank_img_up, 270, 1)
        self.tank_size = self.tank_img_up.get_size()

    def __wipe(self, window):
        """
        清除绘制
        """
        pygame.draw.rect(window, (0, 0, 0),
                         (self.tank_pos[0], self.tank_pos[1],
                          self.tank_size[0] + 3, self.tank_size[1] + 3))

    def set_origin(self, window, coord):
        """
        在初始点绘制坦克
        """
        self.tank_pos = [coord[0], coord[1]]
        self.tank_state = UP
        window.blit(self.tank_img_up, self.tank_pos)
        self.__ifmove = False
        self.__ifshot = False

    def stop(self):
        """
        停止持续移动
        """
        self.__ifmove = False

    def start(self):
        """
        开始持续移动
        """
        self.__ifmove = True

    def move(self, window, ori, bricks, tanks):
        """
        控制坦克移动
        """
        if not self.__ifshot and self.__ifmove:
            if ori == self.tank_state:
                if self.tank_state == UP and self.tank_pos[1] >= SPEED:
                    self.tank_pos[1] -= SPEED
                    if self.__check_overlap(bricks, tanks):
                        self.tank_pos[1] += SPEED
                    else:
                        self.__wipe(window)
                        window.blit(self.tank_img_up, self.tank_pos)

                elif self.tank_state == DOWN and self.tank_pos[1] < WIN_SIZE[1] - self.tank_size[1] - SPEED:
                    self.tank_pos[1] += SPEED
                    if self.__check_overlap(bricks, tanks):
                        self.tank_pos[1] -= SPEED
                    else:
                        self.__wipe(window)
                        window.blit(self.tank_img_down, self.tank_pos)

                elif self.tank_state == LEFT and self.tank_pos[0] >= SPEED:
                    self.tank_pos[0] -= SPEED
                    if self.__check_overlap(bricks, tanks):
                        self.tank_pos[0] += SPEED
                    else:
                        self.__wipe(window)
                        window.blit(self.tank_img_left, self.tank_pos)

                elif self.tank_state == RIGHT and self.tank_pos[0] < WIN_SIZE[0] - self.tank_size[0] - SPEED:
                    self.tank_pos[0] += SPEED
                    if self.__check_overlap(bricks, tanks):
                        self.tank_pos[0] -= SPEED
                    else:
                        self.__wipe(window)
                        window.blit(self.tank_img_right, self.tank_pos)
            else:
                self.tank_state = ori
                self.__wipe(window)

                if ori == UP:
                    window.blit(self.tank_img_up, self.tank_pos)

                elif ori == DOWN:
                    window.blit(self.tank_img_down, self.tank_pos)

                elif ori == LEFT:
                    window.blit(self.tank_img_left, self.tank_pos)

                elif ori == RIGHT:
                    window.blit(self.tank_img_right, self.tank_pos)
        else:
            pass

    def get_shot(self):
        """
        被击中
        """
        self.__ifmove = False
        self.__ifshot = True
        self.__shotcount = 0

    def if_shot(self):
        """
        返回是否被击中状态
        """
        if self.__ifshot and self.__shotcount > 10:
            return True
        else:
            return False

    def __draw_shot(self, window):
        """
        绘制被击中效果
        """
        if self.__shotcount < 10:
            self.__shotcount += 1

            if self.tank_state == UP:
                window.blit(self.tank_img_up, self.tank_pos)
            elif self.tank_state == DOWN:
                window.blit(self.tank_img_down, self.tank_pos)
            elif self.tank_state == LEFT:
                window.blit(self.tank_img_left, self.tank_pos)
            elif self.tank_state == RIGHT:
                window.blit(self.tank_img_right, self.tank_pos)

            boom_img = pygame.image.load('files/爆炸效果素材.png')
            window.blit(boom_img, self.tank_pos)
        elif self.__shotcount < 15:
            self.__shotcount += 1
            self.__wipe(window)

    def __check_overlap(self, bricks, tanks):
        """
        检测是否与砖墙、其它坦克重叠
            只检测玩家坦克与电脑坦克，以及电脑坦克之间是否重叠
        """
        for i in bricks.brickslist:
            if i.pos[0] - self.tank_size[0] < self.tank_pos[0] < i.pos[0] + bricks.brick_size[0] and \
                    i.pos[1] - self.tank_size[1] < self.tank_pos[1] < i.pos[1] + bricks.brick_size[1]:
                return True

        for i in tanks:
            if i != self:
                if i.tank_pos[0] - self.tank_size[0] < self.tank_pos[0] < i.tank_pos[0] + self.tank_size[0] and \
                        i.tank_pos[1] - self.tank_size[1] < self.tank_pos[1] < i.tank_pos[1] + self.tank_size[1]:
                    return True

        return False

    def fire(self, bullets):
        """
        坦克开炮，将炮弹添加到bullets列表
        """
        if not self.__ifshot:
            if self.tank_state == UP:
                bullet_pos = [self.tank_pos[0] + self.tank_size[0] / 2 - bullets.bullet_size[0] / 2,
                              self.tank_pos[1] - bullets.bullet_size[1]]

            elif self.tank_state == DOWN:
                bullet_pos = [self.tank_pos[0] + self.tank_size[0] / 2 - bullets.bullet_size[0] / 2,
                              self.tank_pos[1] + self.tank_size[1]]

            elif self.tank_state == LEFT:
                bullet_pos = [self.tank_pos[0] - bullets.bullet_size[0],
                              self.tank_pos[1] + self.tank_size[1] / 2 - bullets.bullet_size[1] / 2]

            elif self.tank_state == RIGHT:
                bullet_pos = [self.tank_pos[0] + self.tank_size[0],
                              self.tank_pos[1] + self.tank_size[1] / 2 - bullets.bullet_size[1] / 2]

            newbullet = bulletclass.OneBullet(bullet_pos, self.tank_state)
            bullets.add_bullet(newbullet)

    def update(self, window):
        if self.__ifshot:
            self.__draw_shot(window)

