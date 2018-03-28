# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-12
from dictionary.other.CharType import CharType
from seg.NShort.Path.AtomNode import AtomNode
from seg.common.Vertex import Vertex
from dictionary.CustomDictionary import CustomDictionary
from config import Config
from abc import ABCMeta, abstractmethod
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Segment(object):
    """
    分词器
    是所有分词器的基类
    """
    __metaclass__ = ABCMeta
    CharType()

    # 分词器配置
    def __init__(self):
        # 构造一个分词器
        self.config = Config()

    def seg(self, text):
        """
        分词
        :@param text 待分词文本
        :@return 单词列表
        """
        text = unicode(text, "utf-8")
        charArray = list(text)
        return self.segSentence(charArray)

    @abstractmethod
    def segSentence(self, sentence):
        """
        给一个句子分词
        :@param sentence待分词句子，字符列表
        :@return 单词列表
        """
        pass

    def enablePartOfSpeechTagging(self, enable):
        """
        开启词性标注
        :@param enable
        :@return
        """
        self.config.speechTagging = enable
        return self

    def enableNameRecognize(self, enable):
        """
        开启人名识别
        :@param enable
        :@return
        """
        self.config.nameRecognize = enable
        self.config.updateNerConfig()
        return self

    def enableTranslateNameRecognize(self, enable):
        """
        是否启用音译人名识别
        :@param enable
        :@return
        """
        self.config.translateNameRecognize = enable
        self.config.updateNerConfig()
        return self

    def enableJapaneseNameRecognize(self, enable):
        """
        是否启用日本人名识别
        :@param enable
        :@return
        """
        self.config.japaneseNameRecognize = enable
        self.config.updateNerConfig()
        return self

    def enablePlaceRecognize(self, enable):
        """
        开启地名识别
        :@param enable
        :@return
        """
        self.config.placeRecognize = enable
        self.config.updateNerConfig()
        return self

    def enableOrganizationRecognize(self, enable):
        """
        开启机构名识别
        :@param enable
        :@return
        """
        self.config.organizationRecognize = enable
        self.config.updateNerConfig()
        return self

    def enableOffset(self, enable):
        """
        是否启用偏移量计算（开启后Term.offset才会被计算）
        :@param enable
        :@return
        """
        self.config.offset = enable
        return self

    def enableAllNameEntityRecognize(self, enable):
        """
        是否启用所有的命名实体识别
        :@param enable
        :@return
        """
        self.config.nameRecognize = enable
        self.config.japaneseNameRecognize = enable
        self.config.translateNameRecognize = enable
        self.config.placeRecognize = enable
        self.config.organizationRecognize = enable
        self.config.updateNerConfig()
        return self

    @staticmethod
    def quickAtomSegment(charArray, start, end):
        """
        快速原子分词，希望用这个方法替换掉原来缓慢的方法
        :param charArray:
        :param start:
        :param end:
        :return:
        """
        atomNodeList = []
        offsetAtom = start
        preType = CharType.get(charArray[offsetAtom])
        curType = int()
        offsetAtom += 1
        while offsetAtom < end:
            curType = CharType.get(charArray[offsetAtom])
            if curType != preType:
                if charArray[offsetAtom] == '.' and preType == CharType.CT_NUM:
                    offsetAtom += 1
                    while offsetAtom < end:
                        curType = CharType.get(charArray[offsetAtom])
                        if curType != CharType.CT_NUM:
                            break
                        offsetAtom += 1

                s = ''
                for i in range(start, offsetAtom):
                    s += charArray[i]
                atomNodeList.append(AtomNode().init1(s, preType))
                start = offsetAtom

            preType = curType
            offsetAtom += 1

        if offsetAtom == end:
            s = ''
            for i in range(start, offsetAtom):
                s += charArray[i]
            atomNodeList.append(AtomNode().init1(s, preType))
        return atomNodeList

    @staticmethod
    def combineWords(wordNet, start, end, value):
        """
        将连续的词语合并为一个
        :param wordNet: 词图
        :param start: 起始下标（包含）
        :param end: 结束下标（不包含）
        :param value: 新的属性
        :return:
        """
        # 小优化，如果只有一个词，那就不需要合并，直接应用新属性
        if start + 1 == end:
            wordNet[start].attribute = value
        else:
            sbTerm = ""
            for j in range(start, end):
                if wordNet[j] is None:
                    continue
                realWord = wordNet[j].realword
                sbTerm += realWord
                wordNet[j] = None
            wordNet[start] = Vertex().init4(sbTerm, value)

    @staticmethod
    def combineByCustomDictionary(vertexList):
        wordNet = vertexList
        # DAT合并
        dat = CustomDictionary.dat
        i = 0
        while i < len(wordNet):
            state = 1
            state = dat.stransition(wordNet[i].realword, state)
            if state > 0:
                to = i + 1
                end = to
                value = dat.output(state)
                while to < len(wordNet):
                    state = dat.stransition(wordNet[to].realword, state)
                    if state < 0:
                        break
                    output = dat.output(state)
                    if output is not None:
                        value = output
                        end = to + 1
                    to += 1
                if value is not None:
                    Segment.combineWords(wordNet, i, end, value)
                    i = end - 1
            i += 1

        # BinTrie合并
        if CustomDictionary.trie is not None:
            i = 0
            while i < len(wordNet):
                if wordNet[i] is None:
                    i += 1
                    continue
                state = CustomDictionary.trie.transition(wordNet[i].realword.decode(), 0)
                if state is not None:
                    to = i + 1
                    end = to
                    value = state.getValue()

                    while to < len(wordNet):
                        if wordNet[to] is None:
                            to += 1
                            continue
                        state = state.transition(wordNet[to].realword.decode(), 0)
                        if state is None:
                            break
                        if state.getValue() is not None:
                            value = state.getValue()
                            end = to + 1
                        to += 1

                    if value is not None:
                        Segment.combineWords(wordNet, i, end, value)
                        i = end - 1
                i += 1
        vertexList = []
        for vertex in wordNet:
            if vertex is not None:
                vertexList.append(vertex)

        return vertexList


if __name__ == "__main__":
    seg = Segment().config.ner
