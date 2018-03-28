# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-09

"""
原子分词节点
"""


class AtomNode(object):
    def __init__(self):
        self.sWord = ''
        self.nPOS = int()

    def init1(self, sWord, nPOS):
        self.sWord = sWord
        self.nPOS = nPOS
        return self


