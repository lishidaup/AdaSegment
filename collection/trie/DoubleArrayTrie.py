# coding=utf8
"""
双数组Trie树
"""
import sys, os
from collection.bitset.BitSet import BitSet
from corpus.io.Convert import Convert
from corpus.io.ByteArray import ByteArray
from Utility.ByteUtil import ByteUtil
from Utility.Predefine import Predefine
import numpy as np
import cPickle

reload(sys)
sys.setdefaultencoding('utf-8')


class DoubleArrayTrie(object):
    BUF_SIZE = 1638400
    UNIT_SIZE = 8

    class Node(object):
        def __init__(self):
            self.code = int()
            self.depth = int()
            self.left = int()
            self.right = int()

        def toString(self):
            return "Node{\ncode=%i\n,depth=%i\n,left=%i\n,right=%i}" % (self.code, self.depth, self.left, self.right)

    def __init__(self):
        self.check = []  # int
        self.base = []  # int

        self.used = BitSet(DoubleArrayTrie.BUF_SIZE)  # bitset
        self.size = 0
        self.allocSize = 0
        self.key = []
        self.keySize = int()
        self.length = None
        self.value = []
        self.v = []
        self.progress = int()
        self.nextCheckPos = int()
        self.error_ = 0

    def resize(self, newSize):
        """
         拓展数组
         :param newSize
         :return
        """
        check2 = [0] * int(newSize)
        base2 = [0] * int(newSize)
        if self.allocSize > 0:
            check2[0: self.allocSize] = self.check[0: self.allocSize]
            base2[0: self.allocSize] = self.base[0: self.allocSize]
        self.check = check2
        self.base = base2
        self.allocSize = newSize
        return self.allocSize

    def fetch(self, parent, siblings):
        """
        获取直接相连的子节点
        :param parent: 父节点
        :param siblings: （子）兄弟节点
        :return: 兄弟节点个数
        """
        if self.error_ < 0:
            return 0

        prev = 0

        for i in range(parent.left, parent.right):
            if self.length:
                flag = self.length[i]
            else:
                flag = len(self.key[i].decode())
            if flag < parent.depth:
                continue

            tmp = self.key[i].decode()
            cur = 0
            if self.length:
                flag = self.length[i]
            else:
                flag = len(tmp)
            if flag != parent.depth:
                cur = ord(tmp[parent.depth]) + 1

            if prev > cur:
                self.error_ = -3
                return 0

            if cur != prev or len(siblings) == 0:
                tmp_node = self.Node()
                tmp_node.depth = parent.depth + 1
                tmp_node.code = cur
                tmp_node.left = i
                if len(siblings) != 0:
                    siblings[len(siblings) - 1].right = i

                siblings.append(tmp_node)

            prev = cur

        if len(siblings) != 0:
            siblings[len(siblings) - 1].right = parent.right

        return len(siblings)

    def insert(self, siblings):
        """
         插入节点
         :param siblings 等待插入的兄弟节点
         :return 插入位置
        """
        if self.error_ < 0:
            return 0

        begin = 0
        first = 0
        nonzero_num = 0
        pos = max(siblings[0].code + 1, self.nextCheckPos) - 1

        if self.allocSize <= pos:
            self.resize(pos + 1)

        while True:
            flag = 0

            pos += 1

            if self.allocSize <= pos:
                self.resize(pos + 1)

            if self.check[pos] != 0:
                nonzero_num += 1
                continue

            elif first == 0:
                self.nextCheckPos = pos
                first = 1

            begin = pos - siblings[0].code
            if self.allocSize <= (begin + siblings[len(siblings) - 1].code):
                self.resize(begin + siblings[len(siblings) - 1].code + 65536 * 8)  # ???
            if self.used.get(begin):
                continue

            i = 1
            while i < len(siblings):
                if self.check[begin + siblings[i].code] != 0:
                    flag = 1
                if flag == 1:
                    break
                i += 1
            if flag == 1:
                continue

            break

        if 1.0 * nonzero_num / (pos - self.nextCheckPos + 1) >= 0.95:
            self.nextCheckPos = pos

        self.used.set(begin)

        self.size = max(self.size, begin + siblings[len(siblings) - 1].code + 1)
        for i in range(len(siblings)):
            self.check[begin + siblings[i].code] = begin

        for i in range(len(siblings)):
            new_siblings = []
            if self.fetch(siblings[i], new_siblings) == 0:
                if self.value:
                    self.base[begin + siblings[i].code] = -self.value[siblings[i].left] - 1
                else:
                    self.base[begin + siblings[i].code] = -siblings[i].left - 1

                if self.value and (-self.value[siblings[i].left] - 1) >= 0:
                    self.error_ = -2
                    return 0

                self.progress += 1
            else:
                self.base[begin + siblings[i].code] = self.insert(new_siblings)

        return begin

    def load(self, byteArray, value):
        if bytearray is None:
            return False
        self.size = byteArray.nextInt()
        self.base = [0] * (self.size + 65535)
        self.check = [0] * (self.size + 65535)
        for i in range(self.size):
            self.base[i] = byteArray.nextInt()
            self.check[i] = byteArray.nextInt()

        self.v = value
        self.used = None
        return True

    def load1(self, path, value):
        """
        从磁盘加载，需要额外提供值
        :param path:
        :param value:
        :return:
        """
        if not self.loadBaseAndCheckByFileChannel(path):
            return False
        self.v = value
        return True

    def load2(self, path):
        """
        载入双数组，但是不提供值，此时本trie相当于一个set
        :param path:
        :return:
        """
        return self.loadBaseAndCheckByFileChannel(path)

    def loadBaseAndCheckByFileChannel(self, path):
        try:
            try:
                byte_Arr = cPickle.load(open(path + Predefine.PIC_EXT, 'rb'))
            except Exception, e:
                byte_Arr = ByteArray.createByteArray(path)
                out = file(path + Predefine.PIC_EXT, 'wb')
                cPickle.dump(byte_Arr, out)
            byte_arr = byte_Arr.bytes
            index = 0
            self.size = ByteUtil.bytesHighFirstToInt(byte_arr, index)

            index += 4

            self.base = [0] * (self.size + 65535)  # 多留一些，防止越界
            self.check = [0] * (self.size + 65535)

            for i in range(self.size):
                self.base[i] = ByteUtil.bytesHighFirstToInt(byte_arr, index)
                index += 4
                self.check[i] = ByteUtil.bytesHighFirstToInt(byte_arr, index)
                index += 4
        except Exception, e:
            return False

        return True

    def clear(self):
        self.check = []
        self.base = []
        self.used = None
        self.size = 0
        self.allocSize = 0

    def getUnitSize(self):
        return DoubleArrayTrie.UNIT_SIZE

    def getSize(self):
        return self.size

    def getTotalSize(self):
        return self.size * DoubleArrayTrie.UNIT_SIZE

    def getNonzeroSize(self):

        result = 0
        for i in range(len(self.check)):
            if self.check[i] != 0:
                result += 1

        return result

    def kvbuild(self, key, value):

        if len(key) != len(value):
            print "键的个数与值的个数不一样！"

        if len(key) == 0:
            print "键值个数为0！"
        self.v = np.array(value)

        return self.klvkbuild(key, None, None, len(key))

    def ebuild(self, keyValueSet):
        """
         构建DAT
         :param keyValueSet 注意此entrySet一定要是字典序的！否则会失败
         :return
        """
        keyList = []
        valueList = []
        for key, value in keyValueSet:
            keyList.append(key)
            valueList.append(value)

        return self.kvbuild(keyList, valueList)

    def build(self, keyValueMap):
        """
         方便地构造一个双数组trie树
         :param keyValueMap 升序键值对map
         :return 构造结果
        """
        if not keyValueMap:
            return
        keyValueSet = keyValueMap.items()

        return self.ebuild(keyValueSet)

    def klvkbuild(self, _key, _length, _value, _keySize):
        """
         唯一的构建方法
         :param _key     值set，必须字典序
         :param _length  对应每个key的长度，留空动态获取
         :param _value   每个key对应的值，留空使用key的下标作为值
         :param _keySize key的长度，应该设为_key.size
         :return 是否出错
        """

        if _keySize > len(_key) or _key is None:
            return 0

        self.key = _key
        self.length = _length
        self.keySize = _keySize
        self.value = _value
        self.progress = 0

        self.resize(65536 * 32)

        self.base[0] = 1
        self.nextCheckPos = 0

        root_node = DoubleArrayTrie.Node()
        root_node.left = 0
        root_node.right = self.keySize
        root_node.depth = 0

        siblings = []
        self.fetch(root_node, siblings)
        self.insert(siblings)

        self.used = None
        self.key = None
        self.length = None
        return self.error_

    def open(self, fileName):

        file = open(fileName, 'r')
        self.size = int(os.path.getsize(fileName) / DoubleArrayTrie.UNIT_SIZE)
        self.check = []
        self.base = []

    def save(self, path):
        try:
            out = open(path, 'w+')
            out.writelines(Convert.convert(self.size))
            for i in range(self.size):
                out.writelines(Convert.convert(self.base[i]))
                out.writelines(Convert.convert(self.check[i]))
            out.close()
        except Exception, e:
            return False
        return True

    def save1(self, out):
        """
        将base和check保存下来
        :param out:
        :return:
        """
        try:
            out.writelines(Convert.convert(self.size))
            for i in range(self.size):
                out.writelines(Convert.convert(self.base[i]))
                out.writelines(Convert.convert(self.check[i]))
        except Exception, e:
            return False
        return True

    def get(self, index):
        """
         从值数组中提取下标为index的值<br>
         注意为了效率，此处不进行参数校验
         :param index 下标
         :return 值
        """
        return self.v[index]

    def set(self, key, value):
        """
        更新某个键对应的值
        :param key: 键
        :param value: 值
        :return: 是否成功（失败的原因是没有这个键）
        """
        index = self.exactMatchSearch(key)
        if index >= 0:
            self.v[index] = value
            return True

        return False

    def transition(self, current, c):
        """
        转移状态
        :param current:
        :param c:
        :return:
        """
        b = self.base[current]

        p = b + c + 1
        if b == self.check[p]:
            b = self.base[p]
        else:
            return -1

        return b

    def getSearcher(self, text, offset):

        return self.Searcher(self).init(offset, text)

    def output(self, state):
        """
        检查状态是否对应输出
        :param state: 双数组下标
        :return: 对应的值，null表示不输出
        """
        if state < 0:
            return None

        n = self.base[state]
        if state == self.check[state] and n < 0:
            return self.v[-n - 1]

        return None

    def ctransition(self, c, from1):
        """
        转移状态
        :param c:
        :param from1:
        :return:
        """
        b = from1

        p = b + ord(c.decode()) + 1
        if b == self.check[p]:

            b = self.base[p]
        else:
            return -1

        return b

    def stransition(self, path, from1):
        """
        沿着路径转移状态
        :param path: 路径
        :param from1: 起点（根起点为base[0]=1）
        :return: 转移后的状态（双数组下标）
        """
        b = from1
        for i in range(len(path)):
            p = b + ord(path[i]) + 1
            if b == self.check[p]:
                b = self.base[p]
            else:
                return -1

        p = b
        return p

    def ntransition(self, path):
        """
        沿着节点转移状态
        :param path:
        :return:
        """
        b = self.base[0]

        for i in range(len(path)):
            p = b + ord((path[i].decode())) + 1
            if b == self.check[p]:
                b = self.base[p]
            else:
                return -1

        return b

    def containsKey(self, key):
        return self.exactMatchSearch(key) >= 0

    def exactMatchSearch(self, key):
        """
         精确匹配
         :param key 键
         :return 值
        """

        return self.exactMatchSearch1(key, 0, 0, 0)

    def exactMatchSearch1(self, key, pos, len1, nodePos):
        """
         精确查询
         :param key 键的char数组
         :param pos      char数组的起始位置
         :param len1      键的长度
         :param nodePos  开始查找的位置（本参数允许从非根节点查询）
         :return 查到的节点代表的value ID，负数表示不存在
        """
        key = key.decode()
        if len1 <= 0:
            len1 = len(key)

        nodePos = max(nodePos, 0)
        result = -1

        b = self.base[nodePos]

        for i in range(pos, len1):
            p = b + ord(key[i]) + 1
            if b == self.check[p]:
                b = self.base[p]
            else:
                return result

        p = b
        n = self.base[p]

        if b == self.check[p] and n < 0:
            result = -n - 1
        return result

    def commonPrefixSearch(self, key):
        return self.commonPrefixSearch1(key, 0, 0, 0)

    def commonPrefixSearch1(self, key, pos, len1, nodePos):
        """
        前缀查询
        :param key: 查询字串
        :param pos: 字串的开始位置
        :param len1: 字串长度
        :param nodePos: base中的开始位置
        :return: 一个含有所有下标的list
        """
        if len1 <= 0:
            len1 = len(key)
        if nodePos <= 0:
            nodePos = 0

        result = []

        b = self.base[nodePos]
        i = pos
        while i < len1:
            p = b + ord(key[i].decode()) + 1
            if b == self.check[p]:
                b = self.base[p]
            else:
                return result
            p = b
            n = self.base[p]
            if b == self.check[p] and n < 0:
                result.append(-n - 1)

            i += 1
        return result

    def commonPrefixSearchWithValue(self, key):
        """
        前缀查询，包含值
        :param key: 键
        :return: 键值对列表
        最好用优化版的
        """
        len1 = len(key)
        result = []

        b = self.base[0]

        for i in range(len1):
            p = b
            n = self.base[p]
            if b == self.check[p] and n < 0:
                result.append((str(key[: i]), self.v[-n - 1]))

            p = b + ord(key[i].decode()) + 1

            if b == self.check[p]:
                b = self.base[p]
            else:
                return result

        p = b
        n = self.base[p]
        if b == self.check[p] and n < 0:
            result.append((key, self.v[-n - 1]))

        return result

    def commonPrefixSearchWithValue1(self, keyChars, begin):
        """
        优化的前缀查询，可以复用字符数组
        :param keyChars:
        :param begin:
        :return:
        """
        length = len(keyChars)
        result = []
        b = self.base[0]
        n = int()
        p = int()
        for i in range(begin, length):
            p = b
            n = self.base[p]
            if b == self.check[p] and n < 0:
                result.append(("".join(keyChars[begin:i]), self.v[-n - 1]))

            p = b + ord(keyChars[i].decode()) + 1
            if p < self.size and b == self.check[p]:
                b = self.base[p]
            else:
                return result
        p = b
        n = self.base[p]
        if b == self.check[p] and n < 0:
            result.append(("".join(keyChars[begin:length]), self.v[-n - 1]))
        return result

    def toString(self):

        return "DoubleArrayTrie{size=%i, allocSize=%i, key=%s, keySize=%i, progress=%i, nextCheckPos=%i, error_=%i}" % (
            self.size, self.allocSize, str(self.key), self.keySize, self.progress, self.nextCheckPos, self.error_)

    def size1(self):
        """
        树叶子节点个数
        :return:
        """
        return len(self.v)

    def getCheck(self):
        """
        获取check数组引用，不要修改check
        :return:
        """
        return self.check

    def getBase(self):
        """
        获取base数组引用，不要修改base
        :return:
        """
        return self.base

    def getValueAt(self, index):
        """
        获取index对应的值
        :param index:
        :return:
        """
        return self.v[index]

    def get2(self, key):
        """
         * 精确查询
         *
         * @param key 键
         * @return 值
        """
        index = self.exactMatchSearch(key)
        if index >= 0:
            return self.getValueAt(index)

        return None

    def get1(self, key):

        index = self.exactMatchSearch1(key, 0, len(key), 0)
        if index >= 0:
            return self.getValueAt(index)

        return None

    class Searcher(object):

        def __init__(self, dat_obj):
            self.dat = dat_obj
            # key的起点
            self.begin = int()
            # key的长度
            self.length = int()
            # key的字典序坐标
            self.index = int()
            # key对应的value
            self.value = None
            # 传入的字符数组
            self.charArray = []
            # 上一个node位置
            self.last = int()
            # 上一个字符的下标
            self.i = int()
            # charArray的长度，效率起见，开个变量
            self.arrayLength = int()

        def init(self, offset, charArray):
            """
            构造一个双数组搜索工具
            :param offset    搜索的起始位置
            :param charArray 搜索的目标字符数组
            """
            self.charArray = charArray
            self.i = offset
            self.last = self.dat.base[0]
            self.arrayLength = len(charArray)

            if self.arrayLength == 0:
                self.begin = -1
            else:
                self.begin = offset
            return self

        def next_obj(self):
            """
             * 取出下一个命中输出
             *
             * @return 是否命中，当返回false表示搜索结束，否则使用公开的成员读取命中的详细信息
            """

            b = self.last
            n = int()
            p = int()

            while True:
                if self.i == self.arrayLength:
                    self.begin += 1
                    if self.begin == self.arrayLength:
                        break
                    self.i = self.begin
                    b = self.dat.base[0]
                p = b + ord(self.charArray[self.i]) + 1
                if b == self.dat.check[p]:
                    b = self.dat.base[p]
                else:
                    self.i = self.begin
                    self.begin += 1
                    if self.begin == self.arrayLength:
                        break
                    b = self.dat.base[0]
                    self.i += 1
                    continue

                p = b
                n = self.dat.base[p]
                if b == self.dat.check[p] and n < 0:
                    self.length = self.i - self.begin + 1
                    self.index = -n - 1
                    self.value = self.dat.v[self.index]
                    self.last = b
                    self.i += 1
                    return True

                self.i += 1

            return False


if __name__ == '__main__':
    '''
    inputDict = {'aaa': 'aaa', 'fff': 'fff', 'bbb': 'bbb', '111': '111', '11': '11', 'ccc': 'ddd',
                 'ddd': 'ddd', 'd': 'd'}
    tm = TreeMap(inputDict)
    tm.sort()
    # #print type(tm.result)
    # #print type(tm.result.items())
    # for key, value in tm.result.items():
    #     #print key, value
    #print tm.result.items()
    #print 'hdsj'
    trie = DoubleArrayTrie()
    #print trie.size
    trie.build(tm.result)
    #print trie.size
    '''
    # DoubleArrayTrie().loadBaseAndCheckByFileChannel(
    # "E:/pycharmprojects/IfengNLP/data/dictionary/person/nr.txt.trie.dat")
