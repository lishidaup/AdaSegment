# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-07-11

"""
翻译人名词典，储存和识别翻译人名
"""
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from collection.treemap.TreeMap import TreeMap
from Utility.Predefine import Predefine
from collections import OrderedDict
from Config import Config
from time import time


class TranslatedPersonDictionary(object):
    path = Config.TranslatedPersonDictionaryPath
    trie = None

    def __init__(self):
        start = time()
        if not self.load():
            Predefine.logger.warning("音译人名词典" + TranslatedPersonDictionary.path + "加载失败")
        Predefine.logger.info("音译人名词典%s加载成功,耗时%fms" % (TranslatedPersonDictionary.path, (time() - start) * 1000))
        print "音译人名词典%s加载成功,耗时%fms" % (TranslatedPersonDictionary.path, (time() - start) * 1000)

    def load(self):
        TranslatedPersonDictionary.trie = DoubleArrayTrie()
        if self.loadDat():
            return True
        initdict = OrderedDict()
        # map = TreeMap({})
        # charFrequencyMap = TreeMap({})
        br = open(TranslatedPersonDictionary.path, 'r')
        while 1:
            line = br.readline().encode().strip()
            if not line:
                break
            initdict[line] = True
            '''
            map.put(line, True)
            print line
            # 音译人名常用字词典自动生成
            for c in line.decode():
                # 排除一些过于常用的字
                if c in "不赞":
                    continue
                f = charFrequencyMap.get(c)
                if f is None:
                    f = 0
                charFrequencyMap.put(c, f + 1)
                print c
            '''
        '''
        map.put(".", True)
        # 将常用字也加进去
        for k, v in charFrequencyMap.items():
            if v < 10:
                continue
            map.put(str(k), True)
            print str(k)
        print "开始排序"
        map.sort()
        print "排序完毕"
        '''
        map = TreeMap(initdict)
        Predefine.logger.info("音译人名词典%s开始构建双数组..." % TranslatedPersonDictionary.path)
        print "音译人名词典%s开始构建双数组..." % TranslatedPersonDictionary.path
        TranslatedPersonDictionary.trie.build(map)
        Predefine.logger.info("音译人名词典%s开始编译DAT文件..." % TranslatedPersonDictionary.path)
        print "音译人名词典%s开始编译DAT文件..." % TranslatedPersonDictionary.path
        Predefine.logger.info("音译人名词典%s编译结果:%s" % (TranslatedPersonDictionary.path, self.saveDat()))
        return True

    def loadDat(self):
        return TranslatedPersonDictionary.trie.load2(TranslatedPersonDictionary.path + Predefine.TRIE_EXT)

    def saveDat(self):
        """
        保存dat到磁盘
        :param map:
        :return:
        """
        return TranslatedPersonDictionary.trie.save(TranslatedPersonDictionary.path + Predefine.TRIE_EXT)

    @staticmethod
    def containsKey(key):
        """
        是否包含key
        :param key:
        :return:
        """
        return TranslatedPersonDictionary.trie.containsKey(key)
