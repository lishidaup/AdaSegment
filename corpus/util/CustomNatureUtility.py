# !/usr/bin/env python
# coding=utf-8
"""
运行时动态增加词性工具
"""
from collection.treemap.TreeMap import TreeMap
from Utility.Predefine import Predefine
from corpus.util.EnumBuster import EnumBuster


class CustomNatureUtility(object):
    Predefine.logger.warning("已激活自定义词性功能,用户需对本地环境的兼容性和稳定性负责!\n")
    extraValueMap = TreeMap({})
    enumBuster = EnumBuster()

    def __init__(self):
        pass

    def addNature(self, name):
        """
        增加词性
        @param name 词性名称
        :return: 词性
        """
        customNature = self.extraValueMap.get(name)
        if customNature != None:
            return customNature
        return customNature
