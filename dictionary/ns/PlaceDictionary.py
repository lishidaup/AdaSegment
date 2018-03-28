# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-20

"""
地名识别用的词典，实际上是对两个词典的包装
"""
from collection.AhoCorasick.AhoCorasickDoubleArrayTrie import AhoCorasickDoubleArrayTrie
from dictionary.TransformMatrixDictionary import TransformMatrixDictionary
from dictionary.CoreDictionary import CoreDictionary
from dictionary.ns.NSDictionary import NSDictionary
from collection.treemap.TreeMap import TreeMap
from dictionary.item.EnumItem import EnumItem
from Utility.Predefine import Predefine
from corpus.tag.NS import NS
from Config import Config
from time import time
import numpy as np


class PlaceDictionary(object):
    # 地名词典
    dictionary = NSDictionary()
    # 转移矩阵词典
    transformMatrixDictionary = TransformMatrixDictionary()
    # AC算法用到的Trie树
    trie = AhoCorasickDoubleArrayTrie()
    # 本词典专注的词的ID
    WORD_ID = CoreDictionary.getWordID(Predefine.TAG_PLACE)
    # 本词典专注的词的属性
    ATTRIBUTE = CoreDictionary.get2(WORD_ID)

    def __init__(self):
        self.load()

    def load(self):
        start = time()
        PlaceDictionary.dictionary.load(Config.PlaceDictionaryPath)
        Predefine.logger.info("%s加载成功，耗时%fms" % (Config.PlaceDictionaryPath, (time() - start) * 1000))
        print "%s加载成功，耗时%fms" % (Config.PlaceDictionaryPath, (time() - start) * 1000)
        PlaceDictionary.transformMatrixDictionary = PlaceDictionary.transformMatrixDictionary.init1(NS)
        PlaceDictionary.transformMatrixDictionary.load(Config.PlaceDictionaryTrPath)
        init_dict = {}
        init_dict["CDEH"] = "CDEH"
        init_dict["CDH"] = "CDH"
        init_dict["CH"] = "CH"
        init_dict["GH"] = "GH"
        PlaceDictionary.trie.build(TreeMap(init_dict))

    @staticmethod
    def parsePattern(nsList, vertexList, wordNetOptimum, wordNetAll, pld_obj):
        """
        模式匹配
        :param nsList: 确定的标注序列
        :param wordNetOptimum: 原始的未加角色标注的序列
        :param wordNetAll: 待优化的图
        :return:
        """
        sbPattern = ""
        for ns in nsList:
            sbPattern += str(ns)
        pattern = str(sbPattern)
        wordList = []
        for i in range(len(vertexList)):
            wordList.append(vertexList[i].realword)
        wordArray = np.array(wordList)
        PlaceDictionary.trie.parseText1(pattern, wordArray, pld_obj, wordNetOptimum, wordNetAll)

    @staticmethod
    def isBadCase(name):
        """
        因为任何算法都无法解决100%的问题，总是有一些bad case，这些bad case会以“盖公章 A 1”的形式加入词典中<BR>
        这个方法返回是否是bad case
        :param name:
        :return:
        """
        nrEnumItem = None
        place_list = PlaceDictionary.dictionary.get(name)
        if place_list is not None:
            initdict = dict(place_list)
            nrEnumItem = EnumItem().init3(initdict)
        if nrEnumItem is None:
            return False
        return nrEnumItem.containsLabel(NS.Z)
