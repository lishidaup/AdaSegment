# coding=utf-8
# by lsd 2017-05-12
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from collection.treemap.TreeMap import TreeMap
from corpus.io.ByteArray import ByteArray
from Utility.Predefine import Predefine
from corpus.io.Convert import Convert
from corpus.tag.Nature import Nature
from collections import OrderedDict
from Config import Config
from time import time
import cPickle
import sys


class CoreDictionary(object):
    """
    使用DoubleArrayTrie实现的核心词典
    """

    class Attribute(object):
        """
        核心词典中的词属性
        """

        def __init__(self):
            # 词性列表
            self.nature = [Nature]
            # 词性对应的词频
            self.frequency = [int()]
            self.totalFrequency = int()
            self.logger = Predefine.logger

        def init1(self, size):
            self.nature = [Nature] * int(size)
            self.frequency = [int()] * int(size)
            return self

        def init2(self, nature, frequency):
            self.nature = nature
            self.frequency = frequency
            return self

        def init3(self, nature, frequency):
            self.init1(1)
            self.nature[0] = nature
            self.frequency[0] = frequency
            self.totalFrequency = frequency
            return self

        def init4(self, nature, frequency, totalFrequency):
            self.nature = nature
            self.frequency = frequency
            self.totalFrequency = totalFrequency

        def init5(self, nature):
            """
            使用单个词性，默认词频1000构造
            :param nature:
            :return:
            """
            return self.init3(nature, 1000)

        def create(self, natureWithFrequency):
            try:
                param = natureWithFrequency.strip().split(' ')
                natureCount = len(param) / 2
                attribute = CoreDictionary.Attribute().init1(natureCount)
                for i in range(natureCount):
                    attribute.nature[i] = Nature.valueOf(param[2 * i])
                    attribute.frequency[i] = int(param[1 + 2 * i])
                    attribute.totalFrequency += attribute.frequency[i]
                return attribute
            except:
                self.logger.warning("使用字符串" + natureWithFrequency + "创建词条属性失败！")
                return None

        def bcreate(self, byteArray, natureIndexArray):
            """
            从字节流中加载
            @ param byteArray
            @ param natureIndexArray
            :return:
            """
            currentTotalFrequency = byteArray.nextInt()
            length = byteArray.nextInt()
            attribute = CoreDictionary.Attribute().init1(length)
            attribute.totalFrequency = currentTotalFrequency
            for i in range(length):
                attribute.nature[i] = natureIndexArray[byteArray.nextInt()]
                attribute.frequency[i] = byteArray.nextInt()

            return attribute

        def getNatureFrequency(self, nature):
            """
             获取词性的词频
             @param nature 词性
            :return: 词频
            """
            i = 0
            for pos in self.nature:
                if nature == pos:
                    return self.frequency[i]
                i += 1
            return 0

        def hasNature(self, nature):
            """
            判断是否有某个词性
            @param nature
            :return: boolean
            """
            return self.getNatureFrequency(nature) > 0

        def hasNatureStartsWith(self, prefix):
            """
            是否有以某个前缀开头的词性
            :param prefix: 词性前缀，比如u会查询是否有ude, uzhe等等
            :return: boolean
            """
            for n in self.nature:
                if n.startsWith(prefix):  # ???
                    return True
            return False

        def toString(self):
            """
            nature and frequency to string
            :return: toString result
            """
            result = ""
            for i in range(len(self.nature)):
                result += "%s %s " % (str(self.nature[i]), str(self.frequency[i]))
            return result

        def save(self, out):
            out.writelines(Convert.convert(self.totalFrequency))
            out.writelines(Convert.convert(len(self.nature)))
            for i in range(len(self.nature)):
                out.writelines(Convert.convert(Nature.ordinal(self.nature[i])))
                out.writelines(Convert.convert(self.frequency[i]))

    trie = DoubleArrayTrie()
    attribute = Attribute()
    NR_WORD_ID = None
    NS_WORD_ID = None
    NT_WORD_ID = None
    T_WORD_ID = None
    X_WORD_ID = None
    M_WORD_ID = None
    NX_WORD_ID = None

    def __init__(self):
        self.path = Config.CoreDictionaryPath
        self.logger = Predefine.logger
        self.totalFrequency = 221894

        # 自动加载词典
        start = time()
        if not self.load(self.path):
            self.logger.error('核心词典%s加载失败' % self.path)
            sys.exit(1)
        else:
            end = time()
            self.logger.info('%s加载成功%i个词条，耗时%fms' % (self.path, 2, (end - start) * 1000))

        # 一些特殊的WORD_ID
        CoreDictionary.NR_WORD_ID = CoreDictionary.getWordID(Predefine.TAG_PEOPLE)
        CoreDictionary.NS_WORD_ID = CoreDictionary.getWordID(Predefine.TAG_PLACE)
        CoreDictionary.NT_WORD_ID = CoreDictionary.getWordID(Predefine.TAG_GROUP)
        CoreDictionary.T_WORD_ID = CoreDictionary.getWordID(Predefine.TAG_TIME)
        CoreDictionary.X_WORD_ID = CoreDictionary.getWordID(Predefine.TAG_CLUSTER)
        CoreDictionary.M_WORD_ID = CoreDictionary.getWordID(Predefine.TAG_NUMBER)
        CoreDictionary.NX_WORD_ID = CoreDictionary.getWordID(Predefine.TAG_PROPER)

    @staticmethod
    def get(key):
        """
        获取条目
        :@param key
        :@return
        """
        return CoreDictionary.trie.get2(key)

    def get1(self, wordID):
        """
        获取条目
        :@param key
        :@return
        """
        return self.trie.get(wordID)

    @staticmethod
    def getWordID(a):
        """
        获取词语的ID
        :param a: 词语
        :return: ID，如果不存在，则返回-1
        """
        return CoreDictionary.trie.exactMatchSearch(a)

    def load(self, path):
        self.logger.info("核心词典开始加载：%s" % path)
        print "核心词典开始加载：%s" % path
        if self.loadDat(path):
            return True

        initdict = OrderedDict()
        try:
            f = open(path, 'r')
            line = ''
            MAX_FREQUENCY = 0
            start = time()
            while 1:
                line = f.readline().strip(' \n\t\r')
                if not line:
                    break
                param = line.split('\t')
                natureCount = int((len(param) - 1) / 2)
                attribute = CoreDictionary.Attribute().init1(natureCount)
                for i in range(natureCount):
                    attribute.nature[i] = Nature.valueOf(param[1 + 2 * i])
                    attribute.frequency[i] = int(param[2 + 2 * i])
                    attribute.totalFrequency += attribute.frequency[i]
                initdict[param[0]] = attribute
                MAX_FREQUENCY += attribute.totalFrequency
            map = TreeMap(initdict)
            self.logger.info("核心词典读入词条%i，全部频次%i，耗时%fms" % (map.size(), MAX_FREQUENCY, (time() - start) * 1000))
            print "核心词典读入词条%i，全部频次%i，耗时%fms" % (map.size(), MAX_FREQUENCY, (time() - start) * 1000)
            self.trie.build(map)
            self.logger.info("核心词典加载成功：%i个词条，下面将写入缓存" % self.trie.size1())
            print "核心词典加载成功：%i个词条，下面将写入缓存" % self.trie.size1()

            try:
                out = file(self.path + Predefine.BIN_EXT, 'w+')
                attributeList = map.values()
                out.writelines(Convert.convert(len(attributeList)))
                for attribute in attributeList:
                    out.writelines(Convert.convert(attribute.totalFrequency))
                    out.writelines(Convert.convert(len(attribute.nature)))
                    for i in range(len(attribute.nature)):
                        out.writelines(Convert.convert(Nature.ordinal(attribute.nature[i])))
                        out.writelines(Convert.convert(attribute.frequency[i]))

                self.trie.save(out)
                out.close()
            except Exception, e:
                self.logger.warning("保存失败%s" % str(e))
                return False
        except IOError, e:
            self.logger.warning("核心词典%s不存在或读取错误！" % str(e))
            return False
        return True

    def loadDat(self, path):
        """
        从磁盘加载双数组
        :param path:
        :return:
        """
        start = time()
        try:
            try:
                byteArray = cPickle.load(open(path + Predefine.PIC_EXT, 'rb'))
            except Exception, e:
                byteArray = ByteArray().createByteArray(path + Predefine.BIN_EXT)
                out = file(path + Predefine.PIC_EXT, 'wb')
                cPickle.dump(byteArray, out)
            if byteArray is None:
                return False
            size = byteArray.nextInt()
            # 列表，存储Attribute对象
            attributes = [None] * size
            natureIndexArray = list(Nature)
            for i in range(size):
                # 第一个是全部频次，第二个是词性个数
                currentTotalFrequency = byteArray.nextInt()
                length = byteArray.nextInt()
                attributes[i] = CoreDictionary.Attribute().init1(length)
                attributes[i].totalFrequency = currentTotalFrequency
                for j in range(length):
                    attributes[i].nature[j] = natureIndexArray[byteArray.nextInt()]
                    attributes[i].frequency[j] = byteArray.nextInt()
            if not self.trie.load(byteArray, attributes) or byteArray.hasMore():
                return False
        except Exception, e:
            self.logger.warning("读取失败，问题发生在%s" % (str(e)))
            return False
        print "核心词典加载成功%s，耗时%fms" % (path + Predefine.BIN_EXT, (time() - start) * 1000)
        return True

    @staticmethod
    def get1(key):
        """
        获取条目
        :param key:
        :return:
        """
        return CoreDictionary.trie.get(key)

    @staticmethod
    def get2(wordID):
        """
        获取条目
        :param wordID:
        :return:
        """
        return CoreDictionary.trie.get(wordID)

    def getTermFrequency(self, term):
        """
        获取词频
        :param term:
        :return:
        """
        attribute = self.get1(term)
        if attribute is None:
            return 0
        return attribute.totalFrequency

    def contains(self, key):
        """
        是否包含词语
        :param key:
        :return:
        """
        return self.trie.get(key) is not None


if __name__ == "__main__":
    # print CoreDictionary.attribute.frequency
    # a = CoreDictionary()
    # print CoreDictionary.getWordID("始##始")
    a = CoreDictionary.Attribute().init5(Nature.nrf)
    print a
