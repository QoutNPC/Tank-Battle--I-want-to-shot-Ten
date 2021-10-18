"""
@version:
@author: DQ
@time: 2021-10-13
@file: aiclass.py
@function: 
@modify: 2021-10-18更新按键控制，新增wsad及回车键控制
"""

import pygame
import random
import time

from . import tankclass
from . import bulletclass
from . import brickclass
from . import coordclass

WIN_SIZE = (640, 480)


class GameAI():
    __obj = None  # 单态
    tank_player = None
    play_input_ori = None  # 玩家方向指令
    tanks_ai = None
    tick_ai_op = None  # 敌方坦克行动计时
    tick_ai_fire = None  # 敌方坦克开火计时
    ori_ords = None
    fire_ords = None
    bullets = None
    bricks = None
    __ifover = None  # 游戏是否结束 0-未结束 1-玩家赢 2-电脑赢

    def __new__(cls, *args, **kwargs):
        if not cls.__obj:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self, window):
        # 参数初始化
        self.__ifover = 0

        # 随机生成60个坐标
        coords = coordclass.gen_coord(60)

        # 己方坦克初始化
        self.tank_player = tankclass.Tank('files/坦克1素材.png')
        self.tank_player.set_origin(window, coords.pop())

        # 电脑坦克初始化
        self.tanks_ai = []
        for i in range(10):
            tobj = tankclass.Tank('files/坦克2素材.png')
            tobj.set_origin(window, coords.pop())
            tobj.start()
            self.tanks_ai.append(tobj)
        self.tick_ai_op = time.perf_counter()
        self.tick_ai_fire = time.perf_counter()
        self.ori_ords = coordclass.gen_ori_ords(10)
        self.fire_ords = coordclass.gen_fire_ords(10)

        # 砖墙初始化
        self.bricks = brickclass.Bricks('files/砖墙素材1.png', 'files/砖墙素材2.png')
        for i in range(49):
            bobj = brickclass.OneBrick(coords.pop())
            self.bricks.add_brick(bobj)
        self.bricks.update(window)

        # 子弹初始化
        self.bullets = bulletclass.Bullets('files/子弹素材.png')

    def playinput_keydown(self, key):
        """
        获取玩家控制指令
        """
        if key == pygame.K_UP or key == pygame.K_w:
            self.tank_player.start()
            self.play_input_ori = tankclass.UP

        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.tank_player.start()
            self.play_input_ori = tankclass.DOWN

        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.tank_player.start()
            self.play_input_ori = tankclass.LEFT

        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.tank_player.start()
            self.play_input_ori = tankclass.RIGHT

        elif key == pygame.K_SPACE or key == pygame.K_RETURN:
            self.tank_player.fire(self.bullets)

    def playinput_keyup(self, key):
        if key == pygame.K_UP or key == pygame.K_DOWN or \
                key == pygame.K_LEFT or key == pygame.K_RIGHT or \
                key == pygame.K_w or key == pygame.K_s or \
                key == pygame.K_a or key == pygame.K_d:
            self.tank_player.stop()

    def update(self, window):
        # 玩家坦克移动
        self.tank_player.move(window, self.play_input_ori, self.bricks, self.tanks_ai)

        # 电脑坦克更新移动指令
        if time.perf_counter() - self.tick_ai_op > 1.5:
            self.ori_ords = coordclass.gen_ori_ords(len(self.tanks_ai))
            self.tick_ai_op = time.perf_counter()

        # 电脑坦克维持上一指令的移动状态
        count_ords = 0
        for i in self.tanks_ai:
            i.move(window, self.ori_ords[count_ords], self.bricks, self.tanks_ai)
            count_ords += 1

        # 电脑坦克更新射击指令，并执行
        if time.perf_counter() - self.tick_ai_fire > 0.5:
            self.fire_ords = coordclass.gen_fire_ords(len(self.tanks_ai))

            count_ords = 0
            for i in self.tanks_ai:
                if self.fire_ords[count_ords] == 1:
                    i.fire(self.bullets)

            self.tick_ai_fire = time.perf_counter()

        # 进行子弹判定
        self.bullets.update(window, self.bricks, self.tank_player, self.tanks_ai)
        self.bricks.update(window)
        self.tank_player.update(window)
        for tk in self.tanks_ai:
            tk.update(window)
            if tk.if_shot():
                self.tanks_ai.remove(tk)

        # 进行游戏结果判定
        if self.tank_player.if_shot():
            self.__ifover = 2
        elif len(self.tanks_ai) == 0:
            self.__ifover = 1

        return self.__ifover
