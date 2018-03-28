# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-12

"""
人名识别用的词典，实际上是对两个词典的包装
"""
from collection.AhoCorasick.AhoCorasickDoubleArrayTrie import AhoCorasickDoubleArrayTrie
from dictionary.TransformMatrixDictionary import TransformMatrixDictionary
from dictionary.CoreDictionary import CoreDictionary
from dictionary.nr.NRDictionary import NRDictionary
from collection.treemap.TreeMap import TreeMap
from dictionary.nr.NRPattern import NRPattern
from dictionary.item.EnumItem import EnumItem
from Utility.Predefine import Predefine
from seg.common.Vertex import Vertex
from corpus.tag.Nature import Nature
from corpus.tag.NR import NR
from Config import Config
from time import time
import numpy as np
import sys


class PersonDictionary(object):
    # 人名词典
    dictionary = NRDictionary()
    # 转移矩阵词典
    transformMatrixDictionary = TransformMatrixDictionary()
    # AC算法用到的Trie树
    trie = AhoCorasickDoubleArrayTrie()

    ATTRIBUTE = CoreDictionary.Attribute().init3(Nature.nr, 100)

    def __init__(self):
        self.logger = Predefine.logger
        self.wordArray = None
        self.offsetArray = None
        self.wordNetOptimum = None
        self.wordNetAll = None

        self.init()

    def init(self):
        start = time()
        if not PersonDictionary.dictionary.load(Config.PersonDictionaryPath):
            self.logger.error("人名词典加载失败：%s" % Config.PersonDictionaryPath)
            sys.exit(0)

        PersonDictionary.transformMatrixDictionary.init1(NR)
        PersonDictionary.transformMatrixDictionary.load(Config.PersonDictionaryTrPath)

        initdict = {}
        for pattern in NRPattern:
            initdict[str(pattern)] = pattern
        map = TreeMap(initdict).sort()
        PersonDictionary.trie.build(map)
        self.logger.info("%s加载成功，耗时%fms" % (Config.PersonDictionaryPath, (time() - start) * 1000))

    @staticmethod
    def parsePattern(nrList, vertexList, wordNetOptimum, wordNetAll, pd_obj):
        """
        模式匹配
        :param nrList         确定的标注序列
        :param vertexList     原始的未加角色标注的序列
        :param wordNetOptimum 待优化的图
        :param wordNetAll     全词图
        """
        # 拆分UV
        # 遍历vertextList的下标
        i = -1
        sbPattern = ""
        preNR = NR.A
        backUp = False
        index = 0
        for nr in nrList:
            index += 1
            i += 1
            current = vertexList[i]
            if nr == NR.U:
                if not backUp:
                    i = index - 1
                    backUp = True
                sbPattern += str(NR.K)
                sbPattern += str(NR.B)
                preNR = NR.B

                nowK = current.realword[0:len(current.realword.decode()) - 1]
                nowB = current.realword[len(current.realword.decode()) - 1:]
                vertexList[i] = Vertex().init1(nowK)

                i += 1
                vertexList.insert(i, Vertex().init1(nowB))
                continue
            elif nr == NR.V:
                if not backUp:
                    i = index - 1
                    backUp = True
                if preNR == NR.B:
                    # BE
                    sbPattern += str(NR.E)
                else:
                    # CD
                    sbPattern += str(NR.D)
                sbPattern += str(NR.L)
                # 对串也做一些修改
                # i -= 1
                nowED = current.realword[len(current.realword) - 1:]
                nowL = current.realword[0:len(current.realword) - 1]
                vertexList[i] = Vertex().init1(nowED)
                vertexList.insert(i, Vertex().init1(nowL))
                i += 1
                # i += 1
                continue
            else:

                sbPattern += str(nr)

            # i += 1
            preNR = nr

        pattern = str(sbPattern)
        wordList = []
        for i in range(len(vertexList)):
            wordList.append(vertexList[i].realword)
        wordArray = np.array(wordList)

        offsetArray = [int()] * len(wordArray)
        offsetArray[0] = 0

        for i in range(1, len(wordArray)):
            offsetArray[i] = offsetArray[i - 1] + len(wordArray[i - 1])

        PersonDictionary.trie.parseText(pattern, wordArray, offsetArray, pd_obj, wordNetOptimum, wordNetAll)

    def isBadCase(self, name):
        """
        因为任何算法都无法解决100%的问题，总是有一些bad case，这些bad case会以“盖公章 A 1”的形式加入词典中<BR>
        这个方法返回人名是否是bad case
        :param name:
        :return:
        """
        nrEnumItem = None
        name_list = PersonDictionary.dictionary.get(name)
        if name_list is not None:
            initdict = dict(name_list)
            nrEnumItem = EnumItem().init3(initdict)

        if nrEnumItem is None:
            return False
        return nrEnumItem.containsLabel(NR.A)


if __name__ == "__main__":
    pd = PersonDictionary()
    print pd.trie.output[74][0]
