# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-12

from Segment import Segment
from seg.common.Term import Term

from dictionary.CoreDictionary import CoreDictionary
from seg.common.Vertex import Vertex
from abc import ABCMeta, abstractmethod



class WordBasedGenerativeModelSegment(Segment):
    """
    基于词语n-gram模型的分词器基类
    """
    __metaclass__ = ABCMeta

    def __init__(self):

        Segment.__init__(self)


    def GenerateWordNet(self, wordNetStorage):
        """
        生成一元词网
        :@param wordNetStorage
        """
        charArray = wordNetStorage.charArray
        # 核心词典查询
        searcher = CoreDictionary.trie.getSearcher(charArray, 0)
        while searcher.next_obj():
            s = ''
            for i in range(searcher.begin, searcher.begin + searcher.length):
                s += charArray[i]
            q = Vertex().init2(s, searcher.value, searcher.index)
            wordNetStorage.add(searcher.begin + 1, q)
        # 原子分词，保证图连通
        vertexes = wordNetStorage.getVertexes()

        i = 1
        while i < len(vertexes):
            if len(vertexes[i]) == 0:
                j = i + 1
                while j < len(vertexes) - 1:
                    if not len(vertexes[j]) == 0:
                        break
                    j += 1

                wordNetStorage.add1(i, Segment.quickAtomSegment(charArray, i - 1, j - 1))
                i = j
            else:
                i += len(vertexes[i][len(vertexes[i]) - 1].realword)

    @staticmethod
    def convert(vertexlist, offsetEnabled):
        """
        将一条路径转为最终结果
        :@param vertexList
        :@param offsetEnabled 是否计算offset
        :@return
        """
        assert vertexlist is not None
        assert len(vertexlist) >= 2
        length = len(vertexlist) - 2
        resultList = []
        iterator = iter(vertexlist)
        iterator.next()
        if offsetEnabled:
            offset = 0
            for i in range(length):
                vertex = iterator.next()
                term = WordBasedGenerativeModelSegment.convert2term(vertex)
                term.offset = offset
                offset += term.length()
                resultList.append(term)
        else:
            for i in range(length):
                vertex = iterator.next()
                term = WordBasedGenerativeModelSegment.convert2term(vertex)
                resultList.append(term)
        return resultList

    @staticmethod
    def speechTagging(vertexList):
        """
        词性标注
        :@param vertexList
        """
        pass

    @staticmethod
    def convert2term(vertex):
        return Term(vertex.realword, vertex.guessNature())


if __name__ == '__main__':
    '''
    try:
        wg = WordBasedGenerativeModelSegment()
    except TypeError:
        pass
    '''
    wg = WordBasedGenerativeModelSegment()
