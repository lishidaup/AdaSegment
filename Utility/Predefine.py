# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-18
from __future__ import division
import logging
import os

class Predefine:
    """
    一些预定义的静态变量
    """
    # 工程根目录
    ROOT = os.getcwd() + "/data"
    # 人名nr
    TAG_PEOPLE = "未##人"
    # 地址 ns
    TAG_PLACE = "未##地"
    # 专有名词 nx
    TAG_PROPER = "未##专"
    # 团体名词 nt
    TAG_GROUP = "未##团"
    # 时间 t
    TAG_TIME = "未##时"
    # 字符串 x
    TAG_CLUSTER = "未##串"
    # 数词 m
    TAG_NUMBER = "未##数"
    # 句子的开始 begin
    TAG_BIGIN = "始##始"
    # 结束 end
    TAG_END = "末##末"
    # 其它
    TAG_OTHER = "未##它"

    # 现在总词频25146057
    MAX_FREQUENCY = 25146057
    # 平滑因子
    dTemp = float(1 / MAX_FREQUENCY + 0.00001)
    # 平滑参数
    dSmoothingPara = 0.1
    # 日志组件
    logger = logging.getLogger('AdaSegment')
    # ch = logging.StreamHandler()
    # 创建一个handler，用于输出到控制台
    logger.addHandler(logging.StreamHandler())
    # 二进制文件后缀
    BIN_EXT = '.bin'
    # cPickle文件后缀
    PIC_EXT = '.cPickle'
    # trie树文件后缀名
    TRIE_EXT = ".trie.dat"
    # 值文件后缀名
    VALUE_EXT = ".value.dat"
    # 最大有限正数的常量
    MAX_VALUE = 1.7976931348623157e+308

    # SINGLE byte
    CT_SINGLE = 5
    # delimiter
    CT_DELIMITER = CT_SINGLE + 1
    # Chinese Char
    CT_CHINESE = CT_SINGLE + 2
    # HanYu Pinyin
    CT_LETTER = CT_SINGLE + 3
    # HanYu Pinyin
    CT_NUM = CT_SINGLE + 4
    # HanYu Pinyin
    CT_INDEX = CT_SINGLE + 5
    # Other
    CT_OTHER = CT_SINGLE + 12

    def __init__(self):
        pass
