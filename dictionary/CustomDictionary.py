# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-16
"""
用户自定义词典
"""
from dictionary.CoreDictionary import CoreDictionary
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from collections import OrderedDict
from corpus.io.Convert import Convert
from collection.treemap.TreeMap import TreeMap
from collection.trie.bintrie.BinTrie import BinTrie
from corpus.tag.Nature import Nature
from corpus.io.ByteArray import ByteArray
from Utility.Predefine import Predefine
from Config import Config
from time import time
import cPickle


class CustomDictionary(object):
    # 用于储存用户动态插入词条的二分trie树
    trie = BinTrie()
    dat = DoubleArrayTrie()
    # 第一个是主词典，其他是副词典
    path = Config.CustomDictionaryPath

    start = time()

    def __init__(self):
        CustomDictionary.load()
        pass

    @staticmethod
    def load():
        """
        自动加载词典
        :param mainPath:
        :return:
        """
        start = time()
        if not CustomDictionary.loadMainDictionary(CustomDictionary.path[0]):
            Predefine.logger.warning("自定义词典%s加载失败" % (" ".join(CustomDictionary.path)))
        else:
            Predefine.logger.info("自定义词典加载成功:%i个词条,耗时%fms" % (CustomDictionary.dat.size, (time() - start) * 1000))
            print "自定义词典%s加载成功:%i个词条,耗时%fms" % (
                " ".join(CustomDictionary.path), CustomDictionary.dat.size1(), (time() - start) * 1000)
        return True

    @staticmethod
    def loadMainDictionary(mainPath):
        Predefine.logger.info("自定义词典开始加载:%s" % mainPath)
        print "自定义词典开始加载:%s" % mainPath
        if CustomDictionary.loadDat(mainPath):
            return True
        CustomDictionary.dat = DoubleArrayTrie()

        map = TreeMap({})
        customNatureCollector = set()
        try:
            for p in CustomDictionary.path:
                defaultNature = Nature.n
                Predefine.logger.info("以默认词性[%s]加载自定义词典%s中……" % (str(defaultNature), p))
                print "以默认词性[%s]加载自定义词典%s中……" % (str(defaultNature), p)
                success, map = CustomDictionary.loadtxt(p, defaultNature, map, customNatureCollector)
                if not success:
                    Predefine.logger.warning("失败:%s" % p)
        except IOError, e:
            Predefine.logger.error("自定义词典%s不存在或读取错误!%s" % (mainPath, e))
        except Exception, e:
            Predefine.logger.error("自定义词典%s缓存失败!%s\n" % (mainPath, e))
        if map.size() == 0:
            Predefine.logger.warning("没有加载到任何词条")
            # 当做空白占位符
            map.put(Predefine.TAG_OTHER, None)
        Predefine.logger.info("正在构建DoubleArrayTrie……")
        CustomDictionary.dat.build(map)
        # 缓存成dat文件，下次加载会快很多
        Predefine.logger.info("正在缓存词典为dat文件……")
        # 缓存值文件
        attributeList = []
        for key, value in map.items():
            attributeList.append(value)
        out = file(mainPath + Predefine.BIN_EXT, 'w+')
        # 缓存用户词性
        # IOUtil.writeCustomNature(out, customNatureCollector)
        # 缓存正文
        out.writelines(Convert.convert(len(attributeList)))
        for attribute in attributeList:
            attribute.save(out)
        CustomDictionary.dat.save1(out)
        out.close()

        return True

    @staticmethod
    def loadtxt(path, defaultNature, map, customNatureCollector):
        """
        加载用户词典(追加)
        :param path: 词典路径
        :param defaultNature: 默认词性
        :param map:
        :param customNatureCollector: 收集用户词性
        :return:
        """
        try:
            initdict = OrderedDict()
            br = open(path, 'r')
            while 1:
                line = br.readline().encode().strip()
                if not line:
                    break
                param = line.split(" ")
                natureCount = (len(param) - 1) / 2
                attribute = None
                if natureCount == 0:
                    attribute = CoreDictionary.Attribute().init5(defaultNature)
                else:
                    attribute = CoreDictionary.Attribute().init1(natureCount)
                    for i in range(natureCount):
                        attribute.nature[i] = Nature.valueOf(param[1 + 2 * i])
                        attribute.frequency[i] = int(param[2 + 2 * i])
                        attribute.totalFrequency += attribute.frequency[i]
                initdict[param[0]] = attribute
            map = TreeMap(initdict)
        except Exception, e:
            Predefine.logger.warning("自定义词典%s读取错误%s" % (path, e))
            return False, map
        return True, map

    @staticmethod
    def loadDat(path):
        """
        从磁盘加载双数组
        :param path:
        :return:
        """
        try:
            byteArray = cPickle.load(open(path + Predefine.PIC_EXT, 'rb'))
        except Exception, e:
            byteArray = ByteArray.createByteArray(path + Predefine.BIN_EXT)
            out = file(path + Predefine.PIC_EXT, 'wb')
            cPickle.dump(byteArray, out)

        if byteArray is None:
            return False
        size = byteArray.nextInt()
        # 一种兼容措施，当size小于零表示文件头部储存了-size个用户词性
        if size < 0:
            pass
        attributes = [None] * size
        natureIndexArray = list(Nature)
        for i in range(size):
            # 第一个是全部词频,第二个是词性个数
            currentTotalFrequency = byteArray.nextInt()
            length = byteArray.nextInt()
            attributes[i] = CoreDictionary.Attribute().init1(length)
            attributes[i].totalFrequency = currentTotalFrequency
            for j in range(length):
                attributes[i].nature[j] = natureIndexArray[byteArray.nextInt()]
                attributes[i].frequency[j] = byteArray.nextInt()
        if not CustomDictionary.dat.load(byteArray, attributes):
            return False

        return True

    @staticmethod
    def get(key):
        attribute = CustomDictionary.dat.get(key)
        if attribute is not None:
            return attribute
        if CustomDictionary.trie is None:
            return None
        return CustomDictionary.trie.get(key)


if __name__ == "__main__":
    cd = CustomDictionary()
