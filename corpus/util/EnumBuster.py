# !/usr/bin/env python
# coding=utf-8

from collection.treemap.TreeMap import TreeMap


class EnumBuster(object):
    """
    运行时动态增加词性工具
    """

    def __init__(self):
        self.extraValueMap = TreeMap({})
