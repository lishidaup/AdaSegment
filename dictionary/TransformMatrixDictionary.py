# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-31
"""
转移矩阵词典
"""
from __future__ import division
from Utility.Predefine import Predefine
from corpus.tag.NR import NR
from Config import Config
from time import time
import math


class TransformMatrixDictionary(object):
    def __init__(self):
        self.enumType = None
        # 内部标签下标最大值不超过这个值，用于矩阵创建
        self.ordinaryMax = int()
        # 储存转移矩阵
        self.matrix = [[]]
        # 储存每个标签出现的次数
        self.total = []
        # 所有标签出现的总次数
        self.totalFrequency = int()
        # 隐状态
        self.states = []
        # 初始概率
        self.start_probability = []
        # 转移概率
        self.transititon_probability = [[]]
        self.logger = Predefine.logger

    def init1(self, enumType):
        self.enumType = enumType
        return self

    def load(self, path):
        start = time()
        try:
            br = open(path, 'r')
            # 第一行是矩阵的各个类型
            line = br.readline().encode('utf-8').strip('\n\t\r')
            _param = line.split(',')
            # 为了制表方便，第一个label是废物，所以要抹掉它
            labels = _param[1:]
            ordinaryArray = [0] * len(labels)
            self.ordinaryMax = 0
            for i in range(len(ordinaryArray)):
                ordinaryArray[i] = self.convert(labels[i])
                self.ordinaryMax = max(self.ordinaryMax, ordinaryArray[i])
            self.ordinaryMax += 1
            self.matrix = [[0 for col in range(self.ordinaryMax)] for row in range(self.ordinaryMax)]
            # 描述矩阵
            # line_num = 0
            while 1:
                line = br.readline().encode('utf-8').strip('\n\t\r')
                if not line:
                    break
                paramArray = line.split(',')
                currentOrdinary = self.convert(paramArray[0])
                for i in range(len(ordinaryArray)):
                    self.matrix[currentOrdinary][ordinaryArray[i]] = int(paramArray[i + 1])
            # 需要统计一下每个标签出现的次数
            self.total = [int()] * self.ordinaryMax
            for j in range(self.ordinaryMax):
                self.total[j] = 0
                for i in range(self.ordinaryMax):
                    # 按行累加
                    self.total[j] += self.matrix[j][i]
            for j in range(self.ordinaryMax):
                if self.total[j] == 0:
                    for i in range(self.ordinaryMax):
                        # 按列累加
                        self.total[j] += self.matrix[i][j]
            for j in range(self.ordinaryMax):
                self.totalFrequency += self.total[j]
            # 计算HMM四元组
            self.states = ordinaryArray
            self.start_probability = [float()] * self.ordinaryMax
            for s in self.states:
                frequency = self.total[s] + 1e-8
                self.start_probability[s] = -math.log(frequency / self.totalFrequency)
            self.transititon_probability = [[float() for col in range(self.ordinaryMax)] for row in
                                            range(self.ordinaryMax)]
            for fromnode in self.states:
                for tonode in self.states:
                    frequency = self.matrix[fromnode][tonode] + 1e-8
                    self.transititon_probability[fromnode][tonode] = -math.log(frequency / self.total[fromnode])
            print "加载%s成功，耗时%fms" % (path, (time() - start) * 1000)
        except Exception, e:
            self.logger.warning("读取%s失败%s" % (path, str(e)))

        return True

    def convert(self, label):
        return self.enumType.ordinal(label)

    def getTotalFrequency(self, e):
        return self.total[self.enumType.ordinal(e)]


if __name__ == "__main__":
    transformMatrixDictionary = TransformMatrixDictionary()
    transformMatrixDictionary.init1(NR)
    transformMatrixDictionary.load(Config.PersonDictionaryTrPath)
