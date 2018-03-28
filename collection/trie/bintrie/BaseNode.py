# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-16
"""
节点，统一Trie树根和其他节点的基类
:@param <V> 值
"""
from abc import ABCMeta, abstractmethod
from collection.enum.Enum import Enum


class BaseNode(object):
    __metaclass__ = ABCMeta
    # 节点状态
    Status = Enum([
        # 未指定，用于删除词条
        'UNDEFINED_0',
        # 不是词语的结尾
        'NOT_WORD_1',
        # 是个词语的结尾，并且还可以继续
        'WORD_MIDDLE_2',
        # 是个词语的结尾，并且没有继续
        'WORD_END_3'])

    def __init__(self):
        # 子节点,BaseNode数组
        self.child = []
        # 节点代表的字符 protected char c
        self.c = ''
        # 节点代表的值 protected V value
        self.value = None

    @abstractmethod
    def getChild(self, c):
        """
        获取子节点
        :param c:子节点的char 
        :return: 子节点
        """
        pass

    def getValue(self):
        """
        获取节点对应的值
        :return:值
        """
        return self.value

    def transition(self, path, begin):
        cur = self
        for i in range(begin, len(path)):
            cur = cur.getChild(path[i])
            if cur is None or cur.status == BaseNode.Status.UNDEFINED_0:
                return None
        return cur