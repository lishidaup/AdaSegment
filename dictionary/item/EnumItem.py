# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-31

"""
对标签-频次的封装
"""
from collection.treemap.TreeMap import TreeMap
from collection.enum.Enum import Enum


class EnumItem(Enum):
    def __init__(self):
        Enum.__init__(self)
        self.initdict = {}
        self.labelMap = TreeMap({})  # Treemap()对象

    def getFrequency(self, label):
        frequency = self.labelMap.get(label)
        if frequency is None:
            return 0
        return frequency

    def init1(self, label, frequency):
        self.initdict[label] = frequency
        self.labelMap = TreeMap(self.initdict)
        return self

    def init2(self, *args):
        """
        创建一个条目，其标签频次都是1，各标签由参数指定
        :param args:
        :return:
        """
        for label in args:
            self.initdict[label] = 1
        self.labelMap = TreeMap(self.initdict)
        return self

    def init3(self, initdict):
        self.initdict = initdict
        self.labelMap = TreeMap(self.initdict)
        return self

    def init4(self, initdict):
        self.initdict = initdict
        self.labelMap = TreeMap(self.initdict)
        return self

    def containsLabel(self, label):
        return label in self.labelMap.result.keys()

    @staticmethod
    def create(param):
        if param is None:
            return None
        array = param.split(' ')
        return EnumItem.create1(array)

    @staticmethod
    def create1(param):
        if len(param) % 2 == 0:
            return None

        natureCount = (len(param) - 1) / 2
        entries = [None] * natureCount
        for i in range(natureCount):
            entries[i] = {param[1 + 2 * i]: int(param[2 + 2 * i])}
        return {param[0]: entries}


if __name__ == "__main__":
    a = EnumItem().init1('K', 1).labelMap.items()
