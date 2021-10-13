"""
@version:
@author: DQ
@time: 2021-10-13
@file: main.py
@function: 
@modify: 
"""

import pygame
import time
from packages import *

WIN_SIZE = (640, 480)


class Main():
    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode(WIN_SIZE)
        icon = pygame.image.load('files/坦克1素材.png')
        pygame.display.set_caption('  坦克大战——我要打十个  ')
        pygame.display.set_icon(icon)
        pygame.display.flip()

        # 选项按钮初始化
        button_new = buttonclass.Button('再来一局', (180, 70))
        button_new.set_color()
        button_exit = buttonclass.Button('下次一定', (180, 70))
        button_exit.set_color(c_color_bg_on=[255, 128, 128])

        # 游戏控制器初始化
        ai = aiclass.GameAI(window)

        # 准备进入游戏循环
        game_over = 0
        pygame.display.update()
        tick1 = time.perf_counter()
        tick_all_1 = time.perf_counter()
        while True:
            if game_over == 0:
                if time.perf_counter() - tick1 > 0.02:
                    game_over = ai.update(window)
                    pygame.display.update()
                    tick1 = time.perf_counter()
                tick_all = time.perf_counter() - tick_all_1
            elif game_over == 1:
                banner = buttonclass.Button(f'你赢了，总用时{round(tick_all)}秒', (640, 180))
                banner.set_color(c_color_bg_on=[168, 168, 168], c_color_tx_on=[198, 0, 0])
                banner.draw_on(window, (0, 60))
                button_new.draw_on(window, (90, 280))
                button_exit.draw_on(window, (370, 280))
                pygame.display.update()
            else:
                banner = buttonclass.Button(f'你输了，总用时{round(tick_all)}秒', (640, 180))
                banner.set_color(c_color_bg_on=[168, 168, 168], c_color_tx_on=[0, 0, 68])
                banner.draw_on(window, (0, 60))
                button_new.draw_on(window, (90, 280))
                button_exit.draw_on(window, (370, 280))
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if game_over == 0:
                    if event.type == pygame.KEYDOWN:
                        ai.playinput_keydown(event.key)

                    elif event.type == pygame.KEYUP:
                        ai.playinput_keyup(event.key)

                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mpos = event.pos
                        if 90 < mpos[0] < 90 + 180 and \
                                280 < mpos[1] < 280 + 70:
                            window.fill((0, 0, 0))
                            ai = aiclass.GameAI(window)
                            game_over = 0
                            pygame.display.update()
                            tick1 = time.perf_counter()
                            tick_all_1 = time.perf_counter()

                        elif 370 < mpos[0] < 370 + 180 and \
                                280 < mpos[1] < 280 + 70:
                            exit()


if __name__ == '__main__':
    Main()
