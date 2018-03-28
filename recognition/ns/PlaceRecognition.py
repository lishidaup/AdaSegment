# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-20

"""
地址识别
"""

from dictionary.ns.PlaceDictionary import PlaceDictionary
from dictionary.item.EnumItem import EnumItem
from corpus.tag.Nature import Nature
from algoritm.Viterbi import Viterbi
from operator import itemgetter
from corpus.tag.NS import NS


class PlaceRecognition(object):
    @staticmethod
    def Recognition(pWordSegResult, wordNetOptimum, wordNetAll, pld_obj):
        roleTagList = PlaceRecognition.roleTag(pWordSegResult, wordNetAll)
        '''
        sblog = ""
        iterator = iter(pWordSegResult)
        for n in roleTagList:
            sblog += '['
            sblog += iterator.next().realword
            sblog += " "
            sblog += str(n)
            sblog += ']'
        print "地名角色观察%s" % sblog
        '''

        NSList = PlaceRecognition.viterbiExCompute(roleTagList, NS)

        pWordSegResult1 = []
        for i in pWordSegResult:
            pWordSegResult1.append(i)

        '''
        sblog = ""
        iterator = iter(pWordSegResult)
        sblog += '['
        for n in NSList:
            sblog += iterator.next().realword
            sblog += "/"
            sblog += str(n)
            sblog += ' ,'
        sblog.strip(' ,')
        sblog += ']'
        print "地名角色标注%s" % sblog
        '''

        PlaceDictionary.parsePattern(NSList, pWordSegResult1, wordNetOptimum, wordNetAll, pld_obj)
        return True

    @staticmethod
    def roleTag(vertexList, wordNetAll):
        tagList = []
        for vertex in vertexList:
            if Nature.ns == vertex.getNature() and vertex.getAttribute().totalFrequency <= 1000:
                # 二字地名，认为其可以再接一个后缀或前缀
                if len(vertex.realword) < 3:
                    nsEnumItem = EnumItem().init2(NS.H, NS.G).labelMap.items()
                    tagList.append(nsEnumItem)
                # 否则只可以再加后缀
                else:
                    nsEnumItem = EnumItem().init2(NS.G).labelMap.items()
                    tagList.append(nsEnumItem)
                continue
            # 此处用等效词，更加精准
            NSEnumItem = PlaceDictionary.dictionary.get(vertex.word)
            if NSEnumItem is not None:
                NSEnumItem = sorted(NSEnumItem, key=itemgetter(1), reverse=True)
            if NSEnumItem is None:
                NSEnumItem = EnumItem().init1(NS.Z,
                                              PlaceDictionary.transformMatrixDictionary.getTotalFrequency(
                                                  NS.Z)).labelMap.items()
            tagList.append(NSEnumItem)
        return tagList

    @staticmethod
    def insert(vertexList, tagList, wordNetAll, line, ns):
        vertex = wordNetAll.getFirst(line)
        assert vertex is not None
        vertexList.append(vertex)
        tagList.append(EnumItem().init1(ns, 1000))

    @staticmethod
    def viterbiExCompute(roleTagList, NS):
        """
        维特比算法求解最优标签
        :param roleTagList:
        :return:
        """
        return Viterbi.computeEnum(roleTagList, PlaceDictionary.transformMatrixDictionary, NS)



