"""
@version:
@author: DQ
@time: 2021-10-13
@file: coordclass.py
@function: 
@modify: 
"""

import random


def gen_coord(num=60):
    xyseq = random.sample(range(0, 20 * 15), num)
    coords = []
    for i in xyseq:
        y = i // 20
        x = i - 20 * y
        y *= 32
        x *= 32
        coords.append([x, y])
    return coords

def gen_ori_ords(num):
    ori_ords = []
    for i in range(num):
        ori_ords.append(random.randint(0, 3))
    return ori_ords

def gen_fire_ords(num):
    fire_ords = []
    for i in range(num):
        fire_ords.append(random.randint(0, 1))
    return fire_ords