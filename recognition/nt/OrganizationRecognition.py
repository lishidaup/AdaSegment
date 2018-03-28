# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-25


"""
机构识别
"""
from dictionary.nt.OrganizationDictionary import OrganizationDictionary
from dictionary.item.EnumItem import EnumItem
from corpus.tag.Nature import Nature
from algoritm.Viterbi import Viterbi
from operator import itemgetter
from corpus.tag.NT import NT


class OrganizationRecognition(object):
    @staticmethod
    def Recognition(pWordSegResult, wordNetOptimum, wordNetAll, od_obj):
        roleTagList = OrganizationRecognition.roleTag(pWordSegResult, wordNetAll)

        '''
        sblog = ""
        iterator = iter(pWordSegResult)
        for n in roleTagList:
            sblog += '['
            sblog += iterator.next().realword
            sblog += " "
            sblog += str(n)
            sblog += ']'
        print "机构名角色观察%s" % sblog
        '''

        NTList = OrganizationRecognition.viterbiExCompute(roleTagList)

        pWordSegResult1 = []
        for i in pWordSegResult:
            pWordSegResult1.append(i)
        '''
        sblog = ""
        iterator = iter(pWordSegResult)
        sblog += '['
        for n in NTList:
            sblog += iterator.next().realword
            sblog += "/"
            sblog += str(n)
            sblog += ' ,'
        sblog.strip(' ,')
        sblog += ']'
        print "机构名角色标注%s" % sblog
        '''

        OrganizationDictionary.parsePattern(NTList, pWordSegResult1, wordNetOptimum, wordNetAll, od_obj)
        return True

    @staticmethod
    def roleTag(vertexList, wordNetAll):
        tagList = []

        for vertex in vertexList:

            nature = vertex.guessNature()

            if nature == Nature.nrf:
                if vertex.getAttribute().totalFrequency <= 1000:
                    ntEnumItem = EnumItem().init1(NT.F, 1000).labelMap.items()
                    tagList.append(ntEnumItem)
                    continue
            elif nature in [Nature.ni, Nature.nic, Nature.nis, Nature.nit]:
                initdict = {NT.K: 1000, NT.D: 1000}
                ntEnumItem = EnumItem().init4(initdict).labelMap.items()
                tagList.append(ntEnumItem)
                continue
            elif nature == Nature.m:
                ntEnumItem = EnumItem().init1(NT.M, 1000).labelMap.items()
                tagList.append(ntEnumItem)
                continue

            # 此处用等效词,更加精准
            NTEnumItem = OrganizationDictionary.dictionary.get(vertex.word)
            if NTEnumItem is not None:
                NTEnumItem = sorted(NTEnumItem, key=itemgetter(1), reverse=True)
            if NTEnumItem is None:
                NTEnumItem = EnumItem().init1(NT.Z, OrganizationDictionary.transformMatrixDictionary.getTotalFrequency(
                    NT.Z)).labelMap.items()
            tagList.append(NTEnumItem)
        return tagList

    @staticmethod
    def viterbiExCompute(roleTagList):
        """
        维特比算法求解最优标签
        :param roleTagList:
        :return:
        """
        return Viterbi.computeEnum(roleTagList, OrganizationDictionary.transformMatrixDictionary, NT)
