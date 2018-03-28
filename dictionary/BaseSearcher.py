# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-11

"""
查询字典者
"""

from abc import ABCMeta, abstractmethod


class BaseSearcher(object):
    def __init__(self):
        # 待分词文本的char
        self.c = []
        # 指向当前处理字串的开始位置（前面的已经分词分完了）
        self.offset = int()

    def init1(self, c):
        self.c = c
        return self

    def init2(self, text):
        return self.init1(text.decode())

    @abstractmethod
    def next_item(self):
        """
        分出下一个词
        :return:
        """
        pass

    def getOffset(self):
        """
        获取当前偏移
        :return:
        """
        return self.offset
