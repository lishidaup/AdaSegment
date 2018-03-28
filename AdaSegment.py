# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-11
"""
汉语自然语言处理包
常用接口工具类
"""

import sys
from Config import Config
from seg.Viterbi.ViterbiSegment import ViterbiSegment

reload(sys)
sys.setdefaultencoding('utf-8')


class AdaSegment(object):
    # 开启调试模式（会降低性能）
    def enableDebug(self, enable):
        Config.DEBUG = enable

    @staticmethod
    def newSegment():
        """
        创建一个分词器
        与创建一个分词对象相比，该方法便于版本升级后，保证使用最合适的分词器
        """
        return ViterbiSegment()