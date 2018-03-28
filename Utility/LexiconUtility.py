# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-12
"""
跟词语与词性有关的工具类，可以全局动态修改IfengNLP内部词库
"""
from dictionary.CoreDictionary import CoreDictionary
from dictionary.CustomDictionary import CustomDictionary
from corpus.tag.Nature import Nature


class LexiconUtility:
    """
    从IfengNLP的词库中提取某个单词的属性（包括核心词典和用户词典）
    :@param word 单词
    :@param nature 包含词性与频次的信息
    """

    @staticmethod
    def getAttribute(word):
        """
        获取某个单词的词频
        :@param word
        :@return
        """
        attribute = CoreDictionary.get(word)
        if attribute is not None:
            return attribute
        return CustomDictionary.get(word)

    @staticmethod
    def getFrequency(word):
        """
        获取某个单词的词频
        :@param word
        :@return
        """
        attribute = LexiconUtility.getAttribute(word)
        if attribute is None:
            return 0
        return attribute.totalFrequency

    @staticmethod
    def convertStringToNature(name, customNatureCollector):
        """
        将字符串词性转为Enum词性
        @param name 词性名称
        @param customNatureCollector 一个收集集合
        @return 转换结果
        """
        try:
            return Nature.valueOf(name)
        except Exception, e:
            pass

    def __init__(self):
        pass


if __name__ == "__main__":
    le = LexiconUtility
