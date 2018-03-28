# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-11

"""
日本人名识别
"""
from dictionary.nr.JapanesePersonDictionary import JapanesePersonDictionary
from dictionary.CoreDictionary import CoreDictionary
from dictionary.nr.NRConstant import NRConstant
from Utility.Predefine import Predefine
from corpus.tag.Nature import Nature
from seg.common.Vertex import Vertex


class JapanesePersonRecognition(object):
    @staticmethod
    def Recognition(segResult, wordNetOptimum, wordNetAll):
        """
        执行识别
        :param segResult: 粗分结果
        :param wordNetOptimum: 粗分结果对应的词图
        :param wordNetAll: 全词图
        :return:
        """
        sbName = ""
        appendTimes = 0
        charArray = wordNetAll.charArray
        searcher = JapanesePersonDictionary.getSearcher(charArray)
        entry = None
        activeLine = 1
        preOffset = 0
        entry = searcher.next_item()
        while entry is not None:
            label = entry[1]
            key = entry[0]
            offset = searcher.getOffset()
            if preOffset != offset:
                if appendTimes > 1 and len(sbName) > 2:
                    # 日本人名最短为3字
                    JapanesePersonRecognition.insertName(sbName, activeLine, wordNetOptimum, wordNetAll)
                sbName = ""
                appendTimes = 0
            if appendTimes == 0:
                if label == JapanesePersonDictionary.X:
                    sbName += key
                    appendTimes += 1
                    activeLine = offset + 1
            else:
                if label == JapanesePersonDictionary.M:
                    sbName += key
                    appendTimes += 1
                else:
                    if appendTimes > 1 and len(sbName) > 2:
                        JapanesePersonRecognition.insertName(sbName, activeLine, wordNetOptimum, wordNetAll)
                    sbName = ""
                    appendTimes = 0
            preOffset = offset + len(key)
            entry = searcher.next_item()

        if len(sbName) > 0:
            if appendTimes > 1:
                JapanesePersonRecognition.insertName(sbName, activeLine, wordNetOptimum, wordNetAll)

    @staticmethod
    def isBadCase(name):
        """
        是否是bad case
        :param name:
        :return:
        """
        label = JapanesePersonDictionary.get(name)
        if label is None:
            return False
        return label == JapanesePersonDictionary.A

    @staticmethod
    def insertName(name, activeLine, wordNetOptimum, wordNetAll):
        """
        插入日本人名
        :param name:
        :param activeLine:
        :param wordNetOptimum:
        :param wordNetAll:
        :return:
        """
        if JapanesePersonRecognition.isBadCase(name):
            return
        wordNetOptimum.insert(activeLine, Vertex().initVertex(Predefine.TAG_PEOPLE, name,
                                                              CoreDictionary.Attribute().init5(
                                                                  Nature.nrj), NRConstant.WORD_ID), wordNetAll)
