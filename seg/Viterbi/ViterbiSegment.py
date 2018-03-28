# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-11

"""
Viterbi分词器
也是最短路径分词，最短路径求解采用Viterbi算法
"""
print "数据初始化开始"
import time

start = time.time()

from seg.WordBasedGenerativeModelSegment import WordBasedGenerativeModelSegment
from recognition.nr.PersonRecognition import PersonRecognition
from recognition.nr.TranslatedPersonRecognition import TranslatedPersonRecognition
from recognition.nr.JapanesePersonRecognition import JapanesePersonRecognition
from recognition.ns.PlaceRecognition import PlaceRecognition
from recognition.nt.OrganizationRecognition import OrganizationRecognition
from dictionary.nr.PersonDictionary import PersonDictionary
from dictionary.nr.TranslatedPersonDictionary import TranslatedPersonDictionary
from dictionary.nr.JapanesePersonDictionary import JapanesePersonDictionary
from dictionary.ns.PlaceDictionary import PlaceDictionary
from dictionary.nt.OrganizationDictionary import OrganizationDictionary
from dictionary.CustomDictionary import CustomDictionary
from seg.common.WordNet import WordNet
from abc import ABCMeta


class ViterbiSegment(WordBasedGenerativeModelSegment):
    __metaclass__ = ABCMeta

    def __init__(self):
        WordBasedGenerativeModelSegment.__init__(self)
        if self.config.nameRecognize:
            self.pd = PersonDictionary()
        if self.config.translateNameRecognize:
            TranslatedPersonDictionary()
        if self.config.japaneseNameRecognize:
            JapanesePersonDictionary()
        if self.config.placeRecognize:
            self.pld = PlaceDictionary()
        if self.config.organizationRecognize:
            self.od = OrganizationDictionary()

        CustomDictionary()

    def segSentence(self, sentence):
        """
        :param sentence: 字符数组
        :return: 
        """
        wordNetAll = WordNet().initWordNet1(sentence)

        self.GenerateWordNet(wordNetAll)

        vertexList = self.viterbi(wordNetAll)
        # for i in range(len(vertexList)):
        # print "一元词网：", vertexList[i].realword, vertexList[i].guessNature()
        # 加载用户词典
        vertexList = ViterbiSegment.combineByCustomDictionary(vertexList)

        # 命名实体识别
        if self.config.ner:
            wordNetOptimum = WordNet().initWordNet2(sentence, vertexList)
            preSize = wordNetOptimum.getSize()
            if self.config.nameRecognize:
                PersonRecognition.Recognition(vertexList, wordNetOptimum, wordNetAll, self.pd)
            if self.config.translateNameRecognize:
                TranslatedPersonRecognition.Recognition(vertexList, wordNetOptimum, wordNetAll)
            if self.config.japaneseNameRecognize:
                JapanesePersonRecognition.Recognition(vertexList, wordNetOptimum, wordNetAll)
            if self.config.placeRecognize:
                PlaceRecognition.Recognition(vertexList, wordNetOptimum, wordNetAll, self.pld)
            if self.config.organizationRecognize:
                # 层叠隐马尔可夫——生成输出作为下一级隐马输入
                vertexList = self.viterbi(wordNetOptimum)
                wordNetOptimum.clear()
                wordNetOptimum.addAll(vertexList)
                preSize = wordNetOptimum.size
                OrganizationRecognition.Recognition(vertexList, wordNetOptimum, wordNetAll, self.od)

            if wordNetOptimum.size != preSize:
                vertexList = self.viterbi(wordNetOptimum)

        return self.convert(vertexList, self.config.offset)

    def viterbi(self, wordNet):
        """
        :param wordNet: 
        :return: 
        """
        # 避免生成对象，优化速度
        nodes = wordNet.getVertexes()
        vertexList = []

        for index in range(len(nodes[1])):
            node = nodes[1][index]
            node.updateFrom(nodes[0].getFirst())
        for i in range(1, len(nodes) - 1):
            nodeArray = nodes[i]
            if nodeArray is None:
                continue
            for index in range(len(nodeArray)):
                node = nodeArray[index]
                if node.fromnode is None:
                    continue
                for ind in range(len(nodes[i + len(node.realword.decode())])):
                    to = nodes[i + len(node.realword.decode())][ind]
                    to.updateFrom(node)
        fromnode = nodes[len(nodes) - 1].getFirst()
        while fromnode is not None:
            vertexList.insert(0, fromnode)
            fromnode = fromnode.fromnode

        return vertexList


if __name__ == "__main__":
    '''
    cur = time.time()
    res = ""
    n = 1
    vs = ViterbiSegment()
    # vs.config.japaneseNameRecognize = True
    print "数据加载完毕，耗时%fms" % ((time.time() - start) * 1000)
    path = "E:/pycharmprojects/ner_test_data/titlecontent.sample"
    output_file = file("E:/pycharmprojects/ner_test_data/res_python_1.txt", 'w+')
    file1 = open(path, 'r')
    while 1:
        res = ""
        line = file1.readline().strip()

        if not line:
            break
        for item in line.split('\t'):
            item = list(item.decode())

            termList = vs.segSentence(item)
            m = "["
            for i in termList:
                a = i.word + "/" + i.nature
                m += a + ', '
            m = m.strip(', ')
            m += ']'
            res += m + '\t'
        res = res.strip('\t')
        res += '\n'
        print res
        output_file.writelines(res)
        print n
        n += 1
    output_file.close()

    print "总共用时：", time.time() - cur
    '''
    vs = ViterbiSegment()
    item = "纪念1923年2月在汉口被直系军阀杀害的京汉铁路总工会江岸分会委员长林祥谦(又名林元德)烈士".encode()
    item = list(item.decode())
    termList = vs.segSentence(item)
    m = "["
    for i in termList:
        a = i.word + "/" + i.nature
        m += a + ', '
    m = m.strip(', ')
    m += ']'
    print m





