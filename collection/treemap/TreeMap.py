# coding=utf-8

from heapq import heappush, heappop, heapify
from collections import OrderedDict
from Utility.Predefine import Predefine


class ChineseSort(object):
    def __init__(self, py_dict_path, bh_dict_path):
        self.py_dict = self.load_py_dict(py_dict_path)
        self.bh_dict = self.load_bh_dict(bh_dict_path)

    def load_py_dict(self, py_dict_path):
        result = {}
        py_file = open(py_dict_path, 'r')
        for line in py_file.readlines():
            key, value = line.strip().split('\t')
            result[key] = value
        py_file.close()
        return result

    def load_bh_dict(self, bh_dict_path):
        result = {}
        bh_file = open(bh_dict_path, 'r')
        for line in bh_file.readlines():
            key, value = line.strip().split('\t')
            result[key] = value
        bh_file.close()
        return result

    def search(self, search_dict, data):
        if isinstance(data, str):
            data = unicode(data, 'utf-8')
        return search_dict.get(data.encode('utf-8'))

    def comp_char(self, dataA, dataB):
        if dataA == dataB:
            return -1
        pyA = self.search(self.py_dict, dataA)
        pyB = self.search(self.py_dict, dataB)
        if pyA > pyB:
            return 1
        elif pyA < pyB:
            return 0
        else:
            try:
                bhA = eval(self.search(self.bh_dict, dataA))
            except Exception, e:
                bhA = None
            try:
                bhB = eval(self.search(self.bh_dict, dataB))
            except Exception, e:
                bhB = None
            if bhA > bhB:
                return 1
            elif bhA < bhB:
                return 0
            else:
                return "error"

    def comp(self, dataA, dataB):
        result = None
        charA = dataA.decode("utf-8")
        charB = dataB.decode("utf-8")
        n = min(len(charA), len(charB))
        i = 0
        while i < n:
            result = self.comp_char(charA[i], charB[i])
            if result == -1:
                i = i + 1
                if i == n:
                    result = len(charA) > len(charB)
            else:
                break
        return result

    def sort(self, dataList):
        for i in range(1, len(dataList)):
            data = dataList[i]
            j = i
            while j > 0 and self.comp(dataList[j - 1], data):
                dataList[j] = dataList[j - 1]
                j -= 1
            dataList[j] = data
        return dataList


class TreeMap(object):
    py_dict_path = Predefine.ROOT + '/treemap/py.txt'
    bh_dict_path = Predefine.ROOT + '/treemap/bh.txt'
    cs = ChineseSort(py_dict_path, bh_dict_path)

    def __init__(self, inputDict, py_dict_path=Predefine.ROOT + '/treemap/py.txt',
                 bh_dict_path=Predefine.ROOT + '/treemap/bh.txt'):
        self.result = inputDict

    def size(self):
        return len(self.result)

    def put(self, key, value):
        self.result[key] = value

    def get(self, key):
        if key in self.result:
            return self.result[key]
        else:
            return None

    def values(self):
        return self.result.values()

    def keys(self):
        return self.result.keys()

    def items(self):
        return self.result.items()

    def sort_ascii(self, dataList):
        heap = dataList
        heapify(heap)

        sorted_keys = []
        while heap:
            current_data = heappop(heap)
            sorted_keys.append(current_data)
        return sorted_keys

    def sort_chinese(self, dataList):
        return TreeMap.cs.sort(dataList)

    def sort_long(self):
        inputDict = self.result
        self.result = OrderedDict()
        key_list = inputDict.keys()
        key_list.sort()
        for key in key_list:
            self.result[key] = inputDict[key]
        return self

    def sort(self):
        inputDict = self.result
        asciiKeyList = []
        chineseKeyList = []
        sorted_keys = []
        for key in inputDict:
            key = unicode(key, 'utf-8')
            if key >= u'\u4e00' and key <= u'\u9fa5':
                chineseKeyList.append(key.encode('utf-8'))
            else:
                asciiKeyList.append(key.encode('utf-8'))

        if len(asciiKeyList) > 0:
            sorted_keys += self.sort_ascii(asciiKeyList)
        if len(chineseKeyList) > 0:
            sorted_keys += self.sort_chinese(chineseKeyList)
        asciiKeyList = []
        chineseKeyList = []

        self.result = OrderedDict()
        for key in sorted_keys:
            self.result[key] = inputDict[key]
        return self


if __name__ == '__main__':
    inputDict = {1: 'ggg', 2: '777 ', 4: 'sssssss', 9: '体育', 3: '111', 76: '11', 90: 'ddd',
                 54: 'ddd', 45: 'd'}
    tm = TreeMap(inputDict)
    tm.sort_long()
    tm.put(10, 'abc')
    for key, value in tm.items():
        print key, value
    print '-' * 30
    tm.sort_long()
    for key, value in tm.items():
        print key, value

    print 1 in tm.result.keys()


    tm = TreeMap({})
    inputDict = {"一个心眼儿": 'ggg', "一个萝卜一个坑儿": '777 ', "一从": 'sssssss', "一刬": '体育', "一半天": '111',"一字长蛇阵": '11', "一小儿": 'ddd',
                 "一径": 'ddd', "一把好手": 'd',"一搭两用儿":3}
    tm = TreeMap(inputDict)
    '''
    tm.put("一个心眼儿",2)
    tm.put("一个萝卜一个坑儿",3)
    tm.put("一从", 3)
    tm.put("一刬", 3)
    tm.put("一半天", 3)
    tm.put("一字长蛇阵", 3)
    tm.put("一小儿", 3)
    tm.put("一径", 3)
    tm.put("一把好手", 3)
    tm.put("一搭两用儿", 3)
    tm.sort()
    for key in tm.result:
        print key, tm.result[key]
    '''
    for key, value in tm.items():
        print key, value
    print tm.get("1")
    print tm.size()