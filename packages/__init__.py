"""
@version:
@author: DQ
@time: 2021-10-13
@file: __init__.py.py
@function: 
@modify: 
"""

import os

res = os.listdir('./packages')

newres = []
for i in res:
    if i[0:2] != '__':
        s = i[0:-3]
        newres.append(s)

# print(newres)
__all__ = newres
