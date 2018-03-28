# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-18
"""
顶点
"""
from __future__ import division
from dictionary.CoreDictionary import CoreDictionary
from corpus.tag.Nature import Nature
from Utility.Predefine import Predefine
from Utility.MathTools import MathTools
from Utility.Switch import Switch
from dictionary.CoreBiGramTableDictionary import CoreBiGramTableDictionary


class Vertex(object):
    """
    顶点
    """
    cd = CoreDictionary()
    cbtd = CoreBiGramTableDictionary()

    def __init__(self):
        # 节点对应的词或等效词（如未##数）
        self.word = ''
        # 节点对应的真实词，绝对不含##
        self.realword = ''

        # 词的属性，谨慎修改属性内部的数据，因为会影响到字典
        # 如果要修改，应当new一个Attribute
        self.attribute = None
        # 等效词ID,也是Attribute的下标
        self.wordID = int()
        # 在一维顶点数组中的下标，可以视作这个顶点的id
        self.index = int()

        # 到该节点的最短路径的前驱节点
        self.fromnode = None
        # 最短路径对应的权重
        self.weight = float()

    @staticmethod
    def newB():
        return Vertex().initVertex(Predefine.TAG_BIGIN, ' ',
                                   CoreDictionary.Attribute().init3(Nature.begin, Predefine.MAX_FREQUENCY / 10),
                                   CoreDictionary.getWordID(Predefine.TAG_BIGIN))

    @staticmethod
    def newE():
        return Vertex().initVertex(Predefine.TAG_END, ' ',
                                   CoreDictionary.Attribute().init3(Nature.end, Predefine.MAX_FREQUENCY / 10),
                                   CoreDictionary.getWordID(Predefine.TAG_END))

    def updateFrom(self, fromnode):
        weight = fromnode.weight + MathTools.calculateWeight(fromnode, self)
        if self.fromnode is None or self.weight > weight:
            self.fromnode = fromnode
            self.weight = weight

    def initVertex(self, word, realWord, attribute, wordID):
        if attribute is None:
            attribute = CoreDictionary.Attribute().init3(Nature.n, 1)
        self.wordID = wordID
        self.attribute = attribute
        if word is None:
            word = self.compileRealWord(realWord, attribute)

        assert len(realWord) > 0
        self.word = word
        self.realword = realWord.decode()
        return self

    def init1(self, realWord):
        """
        自动构造一个合理的顶点
        :param realword:
        :return:
        """
        return self.initVertex(None, realWord, Vertex.cd.get(realWord), -1)

    def init2(self, realWord, attribute, wordID):
        return self.initVertex(None, realWord, attribute, wordID)

    def init3(self, word, realWord, attribute):
        """
        最复杂的构造函数
        :param word: 编译后的词
        :param realWord: 真实词
        :param attribute: 属性
        :return:
        """
        return self.initVertex(word, realWord, attribute, -1)

    def init4(self, realWord, attribute):
        """
        真实词与编译词相同时候的构造函数
        :param realWord:
        :param attribute:
        :return:
        """
        return self.init3(None, realWord, attribute)

    def compileRealWord(self, realword, attribute):
        if len(attribute.nature) == 1:
            for case in Switch(attribute.nature[0]):
                if case(Nature.nr) or case(Nature.nr1) or case(Nature.nr2) or case(Nature.nrf) or case(Nature.nrj):
                    self.wordID = Vertex.cd.NR_WORD_ID
                    return Predefine.TAG_PEOPLE
                if case(Nature.ns) or case(Nature.nsf):
                    self.wordID = Vertex.cd.NS_WORD_ID
                    return Predefine.TAG_PLACE
                if case(Nature.nx):
                    self.wordID = Vertex.cd.NX_WORD_ID
                    self.attribute = Vertex.cd.get1(Vertex.cd.NX_WORD_ID)
                    return Predefine.TAG_PROPER
                if case(Nature.nt) or case(Nature.ntc) or case(Nature.ntcf) or case(Nature.ntcb) or case(
                        Nature.ntch) or case(Nature.nto) or case(Nature.ntu) or case(Nature.nts) or case(
                    Nature.nth) or case(Nature.nit):
                    self.wordID = Vertex.cd.NT_WORD_ID
                    # self.attribute = Vertex.cd.get1(Vertex.cd.NT_WORD_ID)
                    return Predefine.TAG_GROUP
                if case(Nature.m) or case(Nature.mq):
                    self.wordID = Vertex.cd.M_WORD_ID
                    self.attribute = Vertex.cd.get1(Vertex.cd.M_WORD_ID)
                    return Predefine.TAG_NUMBER
                if case(Nature.x):
                    self.wordID = Vertex.cd.X_WORD_ID
                    self.attribute = Vertex.cd.get1(Vertex.cd.X_WORD_ID)
                    return Predefine.TAG_CLUSTER
                if case(Nature.t):
                    self.wordID = Vertex.cd.T_WORD_ID
                    self.attribute = Vertex.cd.get1(Vertex.cd.T_WORD_ID)
                    return Predefine.TAG_TIME
        return realword

    def getNature(self):
        """
        获取该节点的词性，如果词性还未确定，则返回null
        :return:
        """
        if len(self.attribute.nature) == 1:
            return self.attribute.nature[0]
        return None

    def guessNature(self):
        """
        猜测最可能的词性，也就是这个节点的词性中出现频率最大的那一个词性
        :return:
        """
        return self.attribute.nature[0]

    def getAttribute(self):
        """
        获取词的属性
        :return:
        """
        return self.attribute


if __name__ == "__main__":
    v = Vertex.newB().wordID
    # v.cbtd.getBiFrequency(42996, 95653)
    print v

