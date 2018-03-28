# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-24
"""
地名角色标签 @author lishida
"""
from collection.enum.Enum import Enum

NS = Enum([
    # 地名的上文 我【来到】中关园
    'A',
    # 地名的下文刘家村/和/下岸村/相邻
    'B',
    # 中国地名的第一个字
    'C',
    # 中国地名的第二个字
    'D',
    # 中国地名的第三个字
    'E',
    # 其他整个的地名
    'G',
    # 中国地名的后缀海/淀区
    'H',
    # 连接词刘家村/和/下岸村/相邻
    'X',
    # 其它非地名成分
    'Z',
    # 句子的开头
    'S'
])
