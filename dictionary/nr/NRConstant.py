# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-05

"""
人名识别中常用的一些常量
"""

from dictionary.CoreDictionary import CoreDictionary
from Utility.Predefine import Predefine


class NRConstant(object):
    # 本词典专注的词的ID
    WORD_ID = CoreDictionary.getWordID(Predefine.TAG_PEOPLE)
    # 本词典专注的词的属性
    ATTRIBUTE = CoreDictionary.get2(WORD_ID)
