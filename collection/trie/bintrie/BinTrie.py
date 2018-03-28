# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-16
"""
首字直接分配内存，之后二分动态数组的Trie树，能够平衡时间和空间
"""
from abc import ABCMeta, abstractmethod
from BaseNode import BaseNode


class BinTrie(BaseNode):
    __metaclass__ = ABCMeta

    def __init__(self):
        BaseNode.__init__(self)
        self.size = 0
        # child = new BaseNode[65535 + 1];    //
        # (int)Character.MAX_VALUE
        self.child = [None] * (65535 + 1)
        self.status = self.Status.NOT_WORD_1

    def get(self, key):
        branch = self
        chars = list(key.encode('utf-8', 'ignore'))
        for achar in chars:
            if branch is None:
                return None
            branch = self.getChild(achar)
        if branch is None:
            return None
        # 保证只有成词的节点被返回
        if not (branch.status == self.Status.WORD_END_3 or branch.status == self.Status.WORD_MIDDLE_2):
            return None
        return branch.getValue()

    def getChild(self, c):
        return self.child[0]


if __name__ == "__main__":
    bin = BinTrie()
