# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-11

from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from dictionary.BaseSearcher import BaseSearcher
from collection.treemap.TreeMap import TreeMap
from corpus.io.ByteArray import ByteArray
from Utility.Predefine import Predefine
from abc import ABCMeta, abstractmethod
from corpus.io.Convert import Convert
from collections import OrderedDict
from Config import Config
from time import time
import cPickle


class JapanesePersonDictionary(object):
    path = Config.JapanesePersonDictionaryPath
    trie = None
    # 姓
    X = 'x'
    # 名
    M = 'm'
    # bad case
    A = 'A'

    class Searcher(BaseSearcher):
        """
        最长分词
        """
        __metaclass__ = ABCMeta

        def __init__(self):
            BaseSearcher.__init__(self)
            # 分词从何处开始，这是一个状态
            self.begin = int()
            self.trie = None

        def init_c(self, c, trie):
            self.init1(c)
            self.trie = trie
            return self

        def init_text(self, text, trie):
            self.init2(text)
            self.trie = trie
            return self

        def next_item(self):
            # 保证首次调用找到一个词语
            result = None
            while self.begin < len(self.c):
                entryList = self.trie.commonPrefixSearchWithValue1(self.c, self.begin)
                if len(entryList) == 0:
                    self.begin += 1
                else:
                    result = entryList[-1]
                    self.offset = self.begin
                    self.begin += len(result[0])
                    break
            if result is None:
                return None
            return result

    def __init__(self):
        start = time()
        if not self.load():
            Predefine.logger.warning("日本人名词典%s加载失败" % JapanesePersonDictionary.path)
        Predefine.logger.info("日本人名词典%s加载成功，耗时%fms" % (Config.PinyinDictionaryPath, (time() - start) * 1000))
        print "日本人名词典%s加载成功，耗时%fms" % (Config.PinyinDictionaryPath, (time() - start) * 1000)

    def load(self):
        JapanesePersonDictionary.trie = DoubleArrayTrie()
        if self.loadDat():
            return True
        initdict = OrderedDict()
        br = open(JapanesePersonDictionary.path, 'r')
        while 1:
            line = br.readline().encode().strip()
            if not line:
                break
            param = line.split(" ")
            initdict[param[0]] = param[1]
        map = TreeMap(initdict)
        Predefine.logger.info("日本人名词典%s开始构建双数组..." % JapanesePersonDictionary.path)
        JapanesePersonDictionary.trie.build(map)
        Predefine.logger.info("日本人名词典%s开始编译DAT文件..." % JapanesePersonDictionary.path)
        Predefine.logger.info("日本人名词典%s编译结果：%s" % (JapanesePersonDictionary.path, str(self.saveDat(map))))
        return True

    def loadDat(self):
        try:
            byteArray = cPickle.load(
                open(JapanesePersonDictionary.path + Predefine.VALUE_EXT + Predefine.PIC_EXT, 'rb'))
        except Exception, e:
            byteArray = ByteArray.createByteArray(JapanesePersonDictionary.path + Predefine.VALUE_EXT)
            out = file(JapanesePersonDictionary.path + Predefine.VALUE_EXT + Predefine.PIC_EXT, 'wb')
            cPickle.dump(byteArray, out)

        if byteArray is None:
            return False
        size = byteArray.nextInt()
        valueArray = [None] * size
        for i in range(len(valueArray)):
            valueArray[i] = chr(byteArray.nextChar())
        return JapanesePersonDictionary.trie.load1(JapanesePersonDictionary.path + Predefine.TRIE_EXT, valueArray)

    def saveDat(self, map):
        """
        保存bat到磁盘
        :param map:
        :return:
        """
        out = file(JapanesePersonDictionary.path + Predefine.VALUE_EXT, 'w+')
        out.writelines(Convert.convert(map.size()))
        for k, c in map.items():
            out.writelines(Convert.convert_char(ord(c)))
        out.close()

        return JapanesePersonDictionary.trie.save(JapanesePersonDictionary.path + Predefine.TRIE_EXT)

    @staticmethod
    def getSearcher(charArray):
        return JapanesePersonDictionary.Searcher().init_c(charArray, JapanesePersonDictionary.trie)

    @staticmethod
    def get(key):
        return JapanesePersonDictionary.trie.get2(key)

    @staticmethod
    def containsKey(key, length):
        """
        包含key，且key至少长length
        :param key:
        :param length:
        :return:
        """
        if not JapanesePersonDictionary.trie.containsKey(key):
            return False
        return len(key) >= length

    @staticmethod
    def containsKey1(key):
        """
        是否包含key
        :param key:
        :return:
        """
        return JapanesePersonDictionary.trie.containsKey(key)
