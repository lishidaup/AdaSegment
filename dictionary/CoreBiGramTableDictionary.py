# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-18
"""
核心词典的二元接续词典，采用整型储存，高性能
"""
from Config import Config
from Utility.Predefine import Predefine
from dictionary.CoreDictionary import CoreDictionary
from collection.treemap.TreeMap import TreeMap
from collections import OrderedDict
import cPickle
from time import time
import sys
import re


class CoreBiGramTableDictionary(object):
    """
    描述了词在pair中的范围，具体说来 < br >
    给定一个词idA，从pair[start[idA]]
    开始的start[idA + 1] - start[idA]
    描述了一些接续的频次
    """
    start = []
    # pair[偶数n]表示key，pair[n + 1]=表示frequency
    pair = []
    path = Config.BiGramDictionaryPath
    datPath = Config.BiGramDictionaryPath + ".table" + Predefine.BIN_EXT

    def __init__(self):
        self.logger = Predefine.logger
        self.init()

    def init(self):
        self.logger.info("开始加载二元词典%s.table" % CoreBiGramTableDictionary.path)
        start = time()
        if not self.load(CoreBiGramTableDictionary.path):
            self.logger.error("二元词典加载失败")
            sys.exit(-1)
        else:
            self.logger.info("%s.table加载成功，耗时%fms" % (CoreBiGramTableDictionary.path, (time() - start) * 1000))

    def load(self, path):
        if self.loadDat(CoreBiGramTableDictionary.datPath):
            return True
        # Treemap对象

        map = TreeMap({})
        # map = dict()
        try:
            br = open(path, 'r')

            line = ""
            total = 0
            maxWordId = CoreDictionary.trie.size1()

            line_num = 1
            while 1:
                line = br.readline().strip("\n\r\t ")
                if not line:
                    break

                params = re.split(' ', line)

                twoWord = params[0].split("@")
                a = twoWord[0]

                idA = CoreDictionary.trie.exactMatchSearch(a)
                if idA == -1:
                    continue
                b = twoWord[1]
                idB = CoreDictionary.trie.exactMatchSearch(b)
                if idB == -1:
                    continue
                freq = int(params[1])
                biMap = map.get(idA)
                if biMap is None:
                    biMap = TreeMap({})

                biMap.put(int(idB), freq)
                map.put(int(idA), biMap)

                total += 2
                line_num += 1

            for k, v in map.items():
                map.put(k, v.sort_long())

            map.sort_long()

            br.close()
            CoreBiGramTableDictionary.start = [int()] * (maxWordId + 1)
            # total是连续的个数*2
            CoreBiGramTableDictionary.pair = [int()] * total
            offset = 0
            for i in range(maxWordId):
                bMap = map.get(i)
                if bMap is not None:
                    for k, v in bMap.items():
                        index = offset << 1
                        CoreBiGramTableDictionary.pair[index] = k
                        CoreBiGramTableDictionary.pair[index + 1] = v
                        offset += 1
                CoreBiGramTableDictionary.start[i + 1] = offset

            self.logger.info("二元词典读取完毕:%s")
        except IOError, e:
            self.logger("二元词典%s不存在或读取错误!%s" % (path, e))
            return False
        self.logger.info("开始缓存二元词典到%s" % CoreBiGramTableDictionary.datPath)
        if not self.saveDat(CoreBiGramTableDictionary.datPath):
            self.logger.warning("缓存二元词典到%s失败" % CoreBiGramTableDictionary.datPath)
        return True

    def loadDat(self, path):
        try:
            data = cPickle.load(open(path, "rb"))
            CoreBiGramTableDictionary.start = data[0]
            # 目前CoreNatureDictionary.ngram.txt的缓存依赖于CoreNatureDictionary.txt的缓存
            # 所以这里校验一下二者的一致性，不然可能导致下标越界或者ngram错乱的情况
            if CoreDictionary.trie.size1() != len(CoreBiGramTableDictionary.start) - 1:
                return False
            CoreBiGramTableDictionary.pair = data[1]
        except Exception, e:
            self.logger.warning("尝试载入缓存文件%s发生异常[%s],下面将载入源文件并自动缓存..." % (path, e))
            return False
        return True

    def saveDat(self, path):
        try:
            out = file(path, 'wb')
            cPickle.dump([CoreBiGramTableDictionary.start, CoreBiGramTableDictionary.pair], out)
            out.close()
        except Exception, e:
            self.logger.warning("在缓存%s时发生异常" % e)
            return False
        return True

    @staticmethod
    def getBiFrequency(idA, idB):
        """
        获取共线频次
        :param idA: 第一个词的id
        :param idB: 第二个词的id
        :return: 共现频次
        """
        if idA == -1 or idB == -1:
            # -1表示用户词典，返回正值增加其亲和度
            return 1000

        index = CoreBiGramTableDictionary.binarySearch(CoreBiGramTableDictionary.pair,
                                                       CoreBiGramTableDictionary.start[idA],
                                                       CoreBiGramTableDictionary.start[idA + 1] -
                                                       CoreBiGramTableDictionary.start[idA], idB)
        if index < 0:
            return 0
        index <<= 1
        return CoreBiGramTableDictionary.pair[index + 1]

    @staticmethod
    def binarySearch(a, fromIndex, length, key):
        """
        二分搜索，由于二元接续前一个词固定时，后一个词比较少，所以二分也能取得很高的性能
        :param a:目标数组
        :param fromIndex:开始下标
        :param length:长度
        :param key:词的id
        :return:共现频次
        """
        low = fromIndex
        high = fromIndex + length - 1
        while low <= high:
            mid = (low + high) >> 1
            midVal = a[mid << 1]
            if midVal < key:
                low = mid + 1
            elif midVal > key:
                high = mid - 1
            else:
                # key found
                return mid
        # key not found
        return -(low + 1)


if __name__ == "__main__":
    CoreBiGramTableDictionary()
