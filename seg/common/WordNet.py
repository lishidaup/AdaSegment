# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-18

from Vertex import Vertex
from corpus.tag.Nature import Nature
from Utility.Switch import Switch
from dictionary.CoreDictionary import CoreDictionary
from collection.linkedlist.LinkedList import LinkedList
from Utility.Predefine import Predefine


class WordNet(object):
    def __init__(self):
        # 链表结构，存储Vertex类型对象
        # 节点，每一行都是前缀词，跟图的表示方式不同
        self.vertexes = []
        # 共有多少个节点
        self.size = int()
        # 原始句子对应的数组,存放字符
        self.charArray = []

    def initWordNet1(self, charArray):
        self.charArray = charArray
        self.vertexes = [LinkedList()] * (2 + len(charArray))
        length = len(self.vertexes)
        for i in range(length):
            self.vertexes[i] = LinkedList()
        self.vertexes[0].append(Vertex.newB())
        self.vertexes[length - 1].append(Vertex.newE())
        self.size = 2
        return self

    def initWordNet2(self, charArray, vertexList):
        self.charArray = charArray
        self.vertexes = [LinkedList()] * (len(charArray) + 2)
        for i in range(len(self.vertexes)):
            self.vertexes[i] = LinkedList()
        i = 0
        for vertex in vertexList:
            self.vertexes[i].append(vertex)
            self.size += 1
            i += len(vertex.realword)

        return self

    def initWordNet3(self, wordnet):
        self.vertexes = wordnet.vertexes
        self.size = wordnet.size
        self.charArray = wordnet.charArray
        return self

    def add(self, line, vertex):
        """
        添加顶点
        :param line:行号 
        :param vertex: 顶点
        :return: 
        """

        for index in range(len(self.vertexes[line])):
            oldVertex = self.vertexes[line][index]
            # 保证唯一性
            if len(oldVertex.realword) == len(vertex.realword):
                return

        self.vertexes[line].append(vertex)

        self.size += 1

    def add1(self, line, atomSegment):
        """
        添加顶点，由原子分词顶点添加
        :param line:
        :param atomSegment:
        :return:
        """
        # 将原子部分存入m_segGraph
        offset = 0
        # Init the cost array
        for atomNode in atomSegment:
            # init the word
            sWord = atomNode.sWord
            nature = Nature.n
            id = -1
            for case in Switch(atomNode.nPOS):
                if case(Predefine.CT_CHINESE):
                    break
                if case(Predefine.CT_INDEX) or case(Predefine.CT_NUM):
                    nature = Nature.m
                    sWord = '未##数'
                    id = CoreDictionary.M_WORD_ID
                    break
                if case(Predefine.CT_DELIMITER) or case(Predefine.CT_OTHER):
                    nature = Nature.w
                    break
                if case(Predefine.CT_SINGLE):
                    nature = Nature.nx
                    sWord = '未##串'
                    id = CoreDictionary.X_WORD_ID
                    break
                if case():
                    break
            # 这些通用符的量级都在10万左右
            self.add(line + offset,
                     Vertex().initVertex(sWord, atomNode.sWord, CoreDictionary.Attribute().init3(nature, 10000), id))
            offset += len(atomNode.sWord)

    def get(self, line, length):
        for i in range(len(self.vertexes[line])):
            vertex = self.vertexes[line][i]
            if len(vertex.realword) == length:
                return vertex
        return None

    def get1(self, line):
        """
        获取某一行的所有节点
        :param line:行号
        :return:一个数组
        """
        return self.vertexes[line]

    def getFirst(self, line):
        """
        获取某一行的第一个节点
        :param line:
        :return:
        """
        iterator = iter(self.vertexes[line])

        res = iterator.next()

        return res

    def insert(self, line, vertex, wordNetAll):
        """
        添加顶点，同时检查此顶点是否悬孤，如果悬孤则自动补全
        :param line:
        :param vertex:
        :param wordNetAll:这是一个完全的词图
        :return:
        """
        for i in range(len(self.vertexes[line])):
            oldVertex = self.vertexes[line][i]
            if len(oldVertex.realword) == len(vertex.realword):
                return
        self.vertexes[line].append(vertex)
        self.size += 1
        # 保证连接
        l = line - 1
        while l > 1:
            if self.get(l, 1) is None:
                first = wordNetAll.getFirst(l)
                if first is None:
                    break
                self.vertexes[l].append(first)
                self.size += 1
                if len(self.vertexes[l]) > 1:
                    break
            else:
                break
            l -= 1
        # 首先保证这个词语可直达

        l = line + len(vertex.realword)

        if len(self.get1(l)) == 0:
            targetLine = wordNetAll.get1(l)
            if targetLine is None or len(targetLine) == 0:
                return

            self.vertexes[l].addAll(targetLine)
            self.size += len(targetLine)
        # 直达之后一直往后
        l += 1
        while l < len(self.vertexes):
            # l += 1
            if len(self.get1(l)) == 0:
                first = wordNetAll.getFirst(l)
                if first is None:
                    break
                self.vertexes[l].append(first)
                self.size += 1
                if len(self.vertexes[l]) > 1:
                    break
            else:
                break
            l += 1

    def getSize(self):
        return self.size

    def getVertexes(self):
        return self.vertexes

    def clear(self):
        """
        清空词图
        :return:
        """
        for vertexList in self.vertexes:
            vertexList.clear()

        self.size = 0

    def addAll(self, vertexList):
        """
        全自动添加顶点
        :param vertexList:
        :return:
        """
        i = 0
        for vertex in vertexList:
            self.add(i, vertex)
            i += len(vertex.realword)


if __name__ == "__main__":
    print type(WordNet().initWordNet1(['S']))
