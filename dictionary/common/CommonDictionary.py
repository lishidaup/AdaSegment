# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-18

"""
通用的词典，对应固定格式的词典
"""
from abc import ABCMeta, abstractmethod
from Utility.Predefine import Predefine
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from collection.treemap.TreeMap import TreeMap
from time import time
import re


class CommonDictionary(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.trie = DoubleArrayTrie()
        self.logger = Predefine.logger

    def load(self, path):
        start = time()
        valueArray = self.onLoadValue(path)
        if valueArray is None:
            self.logger.warning("加载值%s.value.dat失败，耗时%fms" % (path, (time() - start) * 1000))
            return False
        self.logger.info("加载值%s.value.dat成功，耗时%fms" % (path, (time() - start) * 1000))
        print "加载值%s.value.dat成功，耗时%fms" % (path, (time() - start) * 1000)

        start = time()

        if self.loadDat(path + '.trie.dat', valueArray):
            self.logger.info("加载键%s.trie.dat成功，耗时%fms" % (path, (time() - start) * 1000))
            print "加载键%s.trie.dat成功，耗时%fms" % (path, (time() - start) * 1000)
            return True

        keyList = []

        try:
            br = open(path, 'r')
            while 1:
                line = br.readline().encode('utf-8').strip(' \n\t\r')
                if not line:
                    break
                paraArray = line.split(' ')
                keyList.append(paraArray[0])
        except Exception, e:
            self.logger.warning("读取%s失败%s" % (path, str(e)))
        resultcode = self.trie.kvbuild(keyList, valueArray)

        if resultcode != 0:
            self.logger.warning("trie建立失败%i,正在尝试排序后重载" % resultcode)
            initdict = {}
            map = None
            for i in range(len(list(valueArray))):
                initdict[keyList[i]] = valueArray[i]
            map = TreeMap(initdict).sort()
            self.trie.build(map)
            i = 0
            for v in map.values():
                valueArray[i] = v
                i += 1
        self.trie.save(path + '.trie.dat')
        self.logger.info(path + "加载成功")
        return True

    @abstractmethod
    def onLoadValue(self, path):
        """
        实现此方法来加载值
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def onSaveValue(self, valueArray, path):
        """
        :param valueArray:
        :param path:
        :return:
        """
        pass

    def loadDat(self, path, valueArray):
        if self.trie.load1(path, valueArray):
            return True
        return False

    def get(self, key):
        """
         查询一个单词
        :param key:
        :return:单词对应的条目
        """

        return self.trie.get2(key)


if __name__ == "__main__":
    cd = CommonDictionary().load("E:/pycharmprojects/IfengNLP/data/dictionary/person/nr.txt")
