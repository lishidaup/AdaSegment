# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-02

from dictionary.nr.PersonDictionary import PersonDictionary
from dictionary.item.EnumItem import EnumItem
from algoritm.Viterbi import Viterbi
from corpus.tag.Nature import Nature
from Utility.Switch import Switch
from corpus.tag.NR import NR


class PersonRecognition:
    """
    人名识别 @author lishida
    """

    @staticmethod
    def Recognition(pWordSegResult, wordNetOptimum, wordNetAll, pd):
        roleTagList = PersonRecognition.roleObserve(pWordSegResult)

        nrList = PersonRecognition.viterbiComputeSimply(roleTagList, NR)

        pWordSegResult1 = []
        for i in pWordSegResult:
            pWordSegResult1.append(i)
        PersonDictionary.parsePattern(nrList, pWordSegResult1, wordNetOptimum, wordNetAll, pd)

        return True

    @staticmethod
    def roleObserve(wordSegResult):
        """
        角色观察（从模型中加载所有词语对应的角色，允许规则补充）
        :param word_seg_result 粗分结果
        """

        tagList = []
        for vertex in wordSegResult:
            nrEnumItem = PersonDictionary.dictionary.get(vertex.realword)
            if nrEnumItem is None:
                for case in Switch(vertex.guessNature()):
                    if case(Nature.nr):
                        # 有些双名实际上可以构成更长的三名
                        if vertex.getAttribute().totalFrequency <= 1000 and len(vertex.realword) == 2:
                            nrEnumItem = EnumItem().init2(NR.X, NR.G).labelMap.items()
                        else:
                            nrEnumItem = EnumItem().init1(NR.A,
                                                          PersonDictionary.transformMatrixDictionary.getTotalFrequency(
                                                              NR.A)).labelMap.items()
                        break
                    if case(Nature.nnt):
                        # 姓+职位
                        nrEnumItem = EnumItem().init2(NR.G, NR.K).labelMap.items()
                        break
                    if case():
                        # nrEnumItem = [(NR.A, PersonDictionary.transformMatrixDictionary.getTotalFrequency(NR.A))]
                        nrEnumItem = EnumItem().init1(NR.A,
                                                      PersonDictionary.transformMatrixDictionary.getTotalFrequency(
                                                          NR.A)).labelMap.items()
                        break
            tagList.append(nrEnumItem)
        return tagList

    @staticmethod
    def viterbi_compute(role_tag_list):
        """
        维特比算法求解最优标签
        :param role_tag_list
        """

    @staticmethod
    def viterbiComputeSimply(roleTagList, NR):
        """
        简化的维特比算法求解最优标签
        :param role_tag_list
        """
        return Viterbi.computeEnumSimply(roleTagList, PersonDictionary.transformMatrixDictionary, NR)
