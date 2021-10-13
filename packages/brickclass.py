"""
@version:
@author: DQ
@time: 2021-10-13
@file: brickclass.py
@function: 
@modify: 
"""

import pygame

WIN_SIZE = (640, 480)


class OneBrick():
    pos = None  # 位置坐标
    remain_HP = None

    def __init__(self, coord):
        self.pos = [coord[0], coord[1]]
        self.remain_HP = 4


class Bricks():
    __obj = None  # 单态
    brick_img_new = None
    brick_img_broken = None
    brick_size = None
    brickslist = None  # 存储砖墙对象的列表

    def __new__(cls, *args, **kwargs):
        if not cls.__obj:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self, filename_new, filename_broken):
        """
        初始化，传入砖墙素材
        """
        self.brick_img_new = pygame.image.load(filename_new)
        self.brick_img_broken = pygame.image.load(filename_broken)
        self.brick_size = self.brick_img_new.get_size()
        self.brickslist = []

    def add_brick(self, b_obj):
        self.brickslist.append(b_obj)

    def __draw(self, window):
        for i in self.brickslist:
            if i.remain_HP > 2:
                window.blit(self.brick_img_new, i.pos)
            elif i.remain_HP > 0:
                window.blit(self.brick_img_broken, i.pos)
            elif i.remain_HP == 0:
                self.brickslist.remove(i)

    def __wipe(self, window):
        for i in self.brickslist:
            pygame.draw.rect(window, (0, 0, 0),
                             (i.pos[0], i.pos[1],
                              self.brick_size[0], self.brick_size[1]))

    def update(self, window):
        self.__wipe(window)
        self.__draw(window)
