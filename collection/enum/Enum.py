# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-18


class Enum(list):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    def valueOf(self, name):
        if name in self:
            return name
        raise AttributeError

    def values(self):
        return self.values

    def ordinal(self, name):
        if name in self:
            return self.index(name)
        raise AttributeError

    def create(self, name):
        """
        创建自定义词性，如果已有该对应词性，则直接返回已有的词性
        :param name: 字符串词性
        :return: Enum词性
        """
        try:
            return self.valueOf(name)
        except Exception, e:
            return
