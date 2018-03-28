# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-12

"""
一个单词，用户可以直接访问此单词的全部属性
"""
from seg.config import Config
from corpus.tag.Nature import Nature
from Utility.LexiconUtility import LexiconUtility


class Term(object):
    """
    构造一个单词
    :@param word 词语
    :@param nature 词性
    """

    def __init__(self, word, nature):
        # 词语
        self.word = word
        # 词性
        self.nature = nature
        # 在文本中的起始位置（需开启分词器的offset选项）
        self.offset = int()

    def toString(self):
        if Config().ShowTermNature:
            return str(self.word) + '/' + str(self.nature)
        return self.word

    def length(self):
        """
        长度
        :@return
        """
        word = self.word.decode('utf-8')
        return len(word)

    def getFrequency(self):
        """
        获取本词语在IfengNLP词库中的频次
        :@return频次，0代表这是个OOV
        """
        return LexiconUtility.getFrequency(self.word)
