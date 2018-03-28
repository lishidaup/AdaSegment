# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-31

"""
维特比算法
"""

from Utility.Predefine import Predefine
from operator import itemgetter
import math


class Viterbi:
    """
    求解HMM模型，所有概率请提前取对数
     * @param obs     观测序列
     * @param states  隐状态
     * @param start_p 初始概率（隐状态）
     * @param trans_p 转移概率（隐状态）
     * @param emit_p  发射概率 （隐状态表现为显状态的概率）
     * @return 最可能的序列
    """

    @staticmethod
    def computeEnumSimply(roleTagList, transformMatrixDictionary, tag):
        """
        仅仅利用了转移矩阵的“维特比”算法
        :param roleTagList: 观测序列
        :param transformMatrixDictionary: 转移矩阵
        :return: 预测结果
        """
        length = len(roleTagList) - 1
        tagList = []
        iterator = iter(roleTagList)
        start = iterator.next()
        pre = iter(start).next()[0]
        perfect_tag = pre

        # 第一个是确定的
        tagList.append(pre)
        for i in range(length):
            perfect_cost = Predefine.MAX_VALUE
            item = iterator.next()
            for cur in item:
                now = transformMatrixDictionary.transititon_probability[tag.ordinal(pre[0])][
                          tag.ordinal(cur[0])] - math.log(
                    (cur[1] + 1e-8) / transformMatrixDictionary.getTotalFrequency(cur[0]))
                if perfect_cost > now:
                    perfect_cost = now
                    perfect_tag = cur
            pre = perfect_tag
            tagList.append(pre[0])
        return tagList

    @staticmethod
    def computeEnum(roleTagList, transformMatrixDictionary, tag):
        """
        标准版的Viterbi算法，查准率高，效率稍低
        :param roleTagList: 观测序列
        :param transformMatrixDictionary: 转移矩阵
        :return: 预测结果
        """
        length = len(roleTagList) - 1
        tagList = []
        # 滚动数组
        cost = [[], []]
        iterator = iter(roleTagList)
        start = iterator.next()
        pre = iter(set([i[0] for i in start])).next()[0]

        # 第一个是确定的
        tagList.append(pre)

        # 第二个也可以简单地算出来
        preTagSet = set()
        item = iterator.next()
        cost[0] = [float()] * len(item)
        j = 0
        for cur in sorted(item, key=itemgetter(0)):
            cost[0][j] = transformMatrixDictionary.transititon_probability[tag.ordinal(pre[0])][
                             tag.ordinal(cur[0])] - math.log(
                (cur[1] + 1e-8) / transformMatrixDictionary.getTotalFrequency(cur[0]))
            j += 1
        preTagSet = sorted([i[0] for i in item])
        # 第三个开始复杂一些
        for i in range(1, length):
            index_i = i & 1
            index_i_1 = 1 - index_i
            item = iterator.next()
            cost[index_i] = [float()] * len(item)
            perfect_cost_line = Predefine.MAX_VALUE
            k = 0
            curTagSet = sorted([i[0] for i in item], key=lambda x: tag.ordinal(x))
            for cur in sorted(item, key=lambda x: tag.ordinal(x[0])):
                cost[index_i][k] = Predefine.MAX_VALUE
                j = 0
                for p in preTagSet:
                    now = cost[index_i_1][j] + transformMatrixDictionary.transititon_probability[tag.ordinal(p[0])][
                        tag.ordinal(cur[0])] - math.log(
                        (cur[1] + 1e-8) / transformMatrixDictionary.getTotalFrequency(cur[0]))
                    if now < cost[index_i][k]:
                        cost[index_i][k] = now
                        if now < perfect_cost_line:
                            perfect_cost_line = now
                            pre = p

                    j += 1
                    # curTagSet.add(cur[0])

                k += 1
            tagList.append(pre)
            preTagSet = curTagSet
        # 对于最后一个##末##
        tagList.append(tagList[0])
        return tagList
