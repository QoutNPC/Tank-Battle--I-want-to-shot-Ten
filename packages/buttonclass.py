"""
@version:
@author: DQ
@time: 2021-10-12
@file: buttonclass.py
@function: 
@modify: 
"""

import pygame


class Button():
    text = None  # 按钮文本
    size = None  # 按钮大小
    color_bg_on = None  # 按钮ON状态颜色
    color_tx_on = None  # 按钮ON状态文字颜色
    color_bg_off = None  # 按钮OFF状态颜色
    color_tx_off = None  # 按钮OFF状态文字颜色
    text_on = None  # 文字ON渲染
    text_off = None  # 文字OFF渲染

    def __init__(self, c_text, c_size):
        """
        初始化，提供按钮文本和按钮大小
        """
        self.text = c_text
        self.size = c_size

    def set_color(self, c_color_bg_on=[23, 139, 255], c_color_tx_on=[255, 255, 255],
                  c_color_bg_off=[162, 162, 162], c_color_tx_off=[255, 255, 255]):
        """
        设置按钮ON和OFF状态的颜色
        """
        self.color_bg_on = c_color_bg_on
        self.color_tx_on = c_color_tx_on
        self.color_bg_off = c_color_bg_off
        self.color_tx_off = c_color_tx_off

        font = pygame.font.Font('files/YaHei Consolas Hybrid 1.12.ttf', 90)
        self.text_on = font.render(self.text, True, self.color_tx_on)
        self.text_off = font.render(self.text, True, self.color_tx_off)
        text_size = self.text_on.get_size()
        if text_size[0] > self.size[0]:
            self.text_on = pygame.transform.rotozoom(self.text_on, 0,
                                                     (self.size[0] - 2) / text_size[0])
            self.text_off = pygame.transform.rotozoom(self.text_off, 0,
                                                      (self.size[0] - 2) / text_size[0])
            text_size = self.text_on.get_size()

        if text_size[1] > self.size[1]:
            self.text_on = pygame.transform.rotozoom(self.text_on, 0,
                                                     (self.size[1] - 2) / text_size[1])
            self.text_off = pygame.transform.rotozoom(self.text_off, 0,
                                                      (self.size[1] - 2) / text_size[1])

        if text_size[0] * 2 < self.size[0] and text_size[1] * 2 < self.size[1]:
            if (self.size[0] / 1.5) / text_size[0] > (self.size[1] / 1.5) / text_size[1]:
                scale = (self.size[1] / 1.5) / text_size[1]
            else:
                scale = (self.size[0] / 1.5) / text_size[0]

            self.text_on = pygame.transform.rotozoom(self.text_on, 0, scale)
            self.text_off = pygame.transform.rotozoom(self.text_off, 0, scale)

    def draw_on(self, window, coord):
        """
        在指定窗口的指定位置绘制ON状态按钮
        """
        text_size = self.text_on.get_size()
        text_coord = [coord[0] + self.size[0] / 2 - text_size[0] / 2,
                      coord[1] + self.size[1] / 2 - text_size[1] / 2]

        pygame.draw.rect(window, self.color_bg_on,
                         (coord[0], coord[1], self.size[0], self.size[1]))
        window.blit(self.text_on, text_coord)

    def draw_off(self, window, coord):
        """
        在指定窗口的指定位置绘制OFF状态按钮
        """
        text_size = self.text_off.get_size()
        text_coord = [coord[0] + self.size[0] / 2 - text_size[0] / 2,
                      coord[1] + self.size[1] / 2 - text_size[1] / 2]

        pygame.draw.rect(window, self.color_bg_off,
                         (coord[0], coord[1], self.size[0], self.size[1]))
        window.blit(self.text_off, text_coord)
