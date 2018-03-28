# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-11

"""
音译人名识别
"""
from dictionary.nr.TranslatedPersonDictionary import TranslatedPersonDictionary
from dictionary.CoreDictionary import CoreDictionary
from dictionary.nr.NRConstant import NRConstant
from Utility.Predefine import Predefine
from corpus.tag.Nature import Nature
from seg.common.Vertex import Vertex


class TranslatedPersonRecognition(object):
    @staticmethod
    def Recognition(segResult, wordNetOptimum, wordNetAll):
        """
        执行识别
        :param segResult: 粗分结果
        :param wordNetOptimum: 粗分结果对应的词图
        :param wordNetAll: 全词图
        :return:
        """
        sbName = ""
        appendTimes = 0
        i = 0
        # i += 1
        line = 1
        activeLine = 1
        while i < len(segResult) - 1:
            i += 1
            vertex = segResult[i]
            if appendTimes > 0:
                if vertex.guessNature() == Nature.nrf or TranslatedPersonDictionary.containsKey(vertex.realword):
                    sbName += vertex.realword
                    appendTimes += 1
                else:
                    # 识别结束
                    if appendTimes > 1:
                        wordNetOptimum.insert(activeLine, Vertex().initVertex(Predefine.TAG_PEOPLE, sbName,
                                                CoreDictionary.Attribute().init5(
                                                    Nature.nrf), NRConstant.WORD_ID), wordNetAll)
                    sbName = ""
                    appendTimes = 0
            else:
                # nrf和nsf触发识别
                if vertex.guessNature() == Nature.nrf or vertex.getNature() == Nature.nsf:
                    sbName += vertex.realword
                    appendTimes += 1
                    activeLine = line
            line += len(vertex.realword)
