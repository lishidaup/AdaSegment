# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-01

"""
基于双数组Trie树的AhoCorasick自动机
"""
from __future__ import division
from dictionary.nr.NRConstant import NRConstant
from collection.AhoCorasick.State import State
from dictionary.nr.NRPattern import NRPattern
from Utility.Predefine import Predefine
from seg.common.Vertex import Vertex
from Utility.Switch import Switch
import numpy as np
import Queue


class AhoCorasickDoubleArrayTrie(object):
    def __init__(self):
        # 双数组值check
        self.check = None
        # 双数组之base
        self.base = None
        # fail 表
        self.fail = None
        # 输出表,二维数组
        self.output = None
        # 保存value
        self.v = []
        # 每个key的长度
        self.l = None
        # base和check的大小
        self.size = int()

    def parseText(self, text, wordArray, offsetArray, pd_obj, wordNetOptimum, wordNetAll):
        """
        处理文本
        :param text: 文本
        :param processor: 处理器
        :return:
        """
        position = 1
        currentState = 0
        for i in range(len(text)):
            currentState = self.getState(currentState, text[i])
            hitArray = self.output[currentState]

            if hitArray is not None:
                for hit in hitArray:
                    self.hit(position - self.l[hit], position, self.v[hit], wordArray, offsetArray, pd_obj,
                             wordNetOptimum, wordNetAll)
            position += 1

    def parseText1(self, text, wordArray, pld_obj, wordNetOptimum, wordNetAll):
        """
        处理文本
        :param text: 文本
        :param processor: 处理器
        :return:
        """
        position = 1
        currentState = 0
        for i in range(len(text)):
            currentState = self.getState(currentState, text[i])
            hitArray = self.output[currentState]

            if hitArray is not None:
                for hit in hitArray:
                    self.hit1(position - self.l[hit], position, self.v[hit], text, wordArray, pld_obj,
                              wordNetOptimum, wordNetAll)
            position += 1

    def parseText2(self, text, wordArray, od_obj, wordNetOptimum, wordNetAll):
        """
        处理文本
        :param text: 文本
        :param processor: 处理器
        :return:
        """
        position = 1
        currentState = 0
        for i in range(len(text)):
            currentState = self.getState(currentState, text[i])
            hitArray = self.output[currentState]

            if hitArray is not None:
                for hit in hitArray:
                    self.hit2(position - self.l[hit], position, self.v[hit], text, wordArray, od_obj,
                              wordNetOptimum, wordNetAll)
            position += 1

    def getState(self, currentState, character):
        """
        转移状态，支持failure转移
        :param currentState:
        :param character:
        :return:
        """
        # 先按success跳转
        newCurrentState = self.transitionWithRoot(currentState, character)
        # 跳转失败的话，按failure跳转
        while newCurrentState == -1:
            currentState = self.fail[currentState]
            newCurrentState = self.transitionWithRoot(currentState, character)
        return newCurrentState

    def transitionWithRoot(self, nodePos, c):
        """
        c转移，如果是根节点则返回自己
        :param nodePos:
        :param c:
        :return:
        """
        b = self.base[nodePos]
        p = b + ord(c) + 1
        if b != self.check[p]:
            if nodePos == 0:
                return 0
            return -1
        return p

    def hit(self, begin, end, value, wordArray, offsetArray, pd_obj, wordNetOptimum, wordNetAll):
        """
        命中一个模式串
        :param begin: 模式串在母文本中的起始位置
        :param end:   模式串在母文本中的终止位置
        :param value: 模式串对应的值
        :return:      模式串对应的值的下标
        """
        sbName = ''
        for i in range(begin, end):
            sbName += wordArray[i].decode()
        name = sbName
        # 对一些bad case 做出调整
        for case in Switch(value):
            if case(NRPattern.BCD):
                # 姓和最后一个名不可能相等的
                if name[0] == name[2]:
                    return
                break
        if pd_obj.isBadCase(name):
            return
        # print "识别出人名:", name, value
        offset = offsetArray[begin]
        wordNetOptimum.insert(offset,
                              Vertex().initVertex(Predefine.TAG_PEOPLE, name, pd_obj.ATTRIBUTE, NRConstant.WORD_ID),
                              wordNetAll)

    def hit1(self, begin, end, value, pattern, wordArray, pld_obj, wordNetOptimum, wordNetAll):
        """
        命中一个模式串
        :param begin: 模式串在母文本中的起始位置
        :param end:   模式串在母文本中的终止位置
        :param value: 模式串对应的值
        :return:      模式串对应的值的下标
        """
        sbName = ''
        for i in range(begin, end):
            sbName += wordArray[i].decode()
        name = sbName
        # 对一些bad case 做出调整
        if pld_obj.isBadCase(name):
            return
        offset = 0
        for i in range(begin):
            offset += len(wordArray[i].decode())
        wordNetOptimum.insert(offset,
                              Vertex().initVertex(Predefine.TAG_PLACE, name, pld_obj.ATTRIBUTE, pld_obj.WORD_ID),
                              wordNetAll)

    def hit2(self, begin, end, value, pattern, wordArray, od_obj, wordNetOptimum, wordNetAll):
        sbName = ''
        for i in range(begin, end):
            sbName += wordArray[i].decode()
        name = sbName
        # 对一些bad case 做出调整
        if od_obj.isBadCase(name):
            return
        #print "识别出机构名%s %s" % (name, value)
        offset = 0
        for i in range(begin):
            offset += len(wordArray[i].decode())
        wordNetOptimum.insert(offset,
                              Vertex().initVertex(Predefine.TAG_GROUP, name, od_obj.ATTRIBUTE, od_obj.WORD_ID),
                              wordNetAll)

    def build(self, map):
        """
        由一个排序好的map创建
        :param map:
        :return:
        """
        self.Builder(self).build(map)

    class Builder(object):
        """
        构建工具
        """

        def __init__(self, ac_obj):

            self.ac = ac_obj
            # 根节点，仅仅用于构建过程
            self.rootState = State()
            # 是否占用，仅仅用于构建
            self.used = []
            # 下一个插入的位置将从此开始搜索
            self.nextCheckPos = int()
            # 已分配在内存中的大小
            self.allocSize = int()
            # 下一个插入的位置将从此开始搜索
            self.nextCheckPos = int()
            # 键值对的大小
            self.keySize = int()
            # 一个控制增长速度的变量
            self.progress = int()

        def build(self, map):
            """
            由一个排序好的map创建
            :param map:
            :return:
            """
            # 把值保存下来
            self.ac.v = np.array(map.values())
            self.ac.l = [int()] * len(self.ac.v)
            keySet = sorted(set(map.keys()))
            # 构建二分trie树
            self.addAllKeyword(keySet)
            # 在二分trie树的基础上构建双数组trie树
            self.buildDoubleArrayTrie(keySet)
            self.used = None
            # 构建failure表并且合并output表
            self.constructFailuresStates()
            self.rootState = None
            self.loseWeight()

        def addAllKeyword(self, keywordSet):
            i = 0
            for keyword in keywordSet:
                self.addKeyword(keyword, i)
                i += 1

        def addKeyword(self, keyword, index):
            """
            添加一个键
            :param keyword: 键
            :param index: 值的下标
            :return:
            """
            currentState = self.rootState
            for character in list(keyword.decode('utf-8')):
                currentState = currentState.addState(character)
            currentState.addEmit(index)
            self.ac.l[index] = len(keyword)

        def buildDoubleArrayTrie(self, keySet):
            self.progress = 0
            self.keySize = len(keySet)
            # 32个双字节
            self.resize(65536 * 32)

            self.ac.base[0] = 1
            self.nextCheckPos = 0

            root_node = self.rootState

            siblings = []
            self.fetch(root_node, siblings)
            self.insert(siblings)

        def resize(self, newSize):
            """
            扩展数组
            :param newSize:
            :return:
            """
            base2 = [int()] * newSize
            check2 = [int()] * newSize
            used2 = [bool()] * newSize
            if self.allocSize > 0:
                base2[:self.allocSize] = self.ac.base[:self.allocSize]
                check2[:self.allocSize] = self.ac.check[:self.allocSize]
                used2[:self.allocSize] = self.used[:self.allocSize]
            self.ac.base = base2
            self.ac.check = check2
            self.used = used2
            self.allocSize = newSize
            return self.allocSize

        def fetch(self, parent, siblings):
            """
            获取直接相连的子节点
            :param parent: 父节点
            :param siblings: （子）兄弟节点
            :return: 兄弟节点个数
            """
            if parent.isAcceptable():
                # 此节点是parent的子节点，同时具备parent的输出
                fakeNode = State().init1(-(parent.getDepth() + 1))
                fakeNode.addEmit(parent.getLargestValueId())
                siblings.append({0: fakeNode})
            for k, v in parent.getSuccess().items():
                siblings.append({ord(k) + 1: v})
            return len(siblings)

        def insert(self, siblings):
            """
            插入节点
            :param siblings:等待插入的兄弟节点
            :return:插入位置插入位置
            """
            begin = 0
            pos = max(siblings[0].keys()[0] + 1, self.nextCheckPos) - 1
            nonzero_num = 0
            first = 0
            if self.allocSize <= pos:
                self.resize(pos + 1)
            # 此循环体的目标是找出满足base[begin + a1...an]  == 0的n个空闲空间,a1...an是siblings中的n个节点
            while True:
                flag = 0
                pos += 1
                if self.allocSize <= pos:
                    self.resize(pos + 1)
                if self.ac.check[pos] != 0:
                    nonzero_num += 1
                    continue
                elif first == 0:
                    self.nextCheckPos = pos
                    first = 1
                # 当前位置离第一个兄弟节点的距离
                begin = pos - siblings[0].keys()[0]
                if self.allocSize <= (begin + siblings[len(siblings) - 1].keys()[0]):
                    # progress can be zero // 防止progress产生除零错误
                    if 1.05 > 1.0 * self.keySize / (self.progress + 1):
                        l = 1.05
                    else:
                        l = 1.0 * self.keySize / (self.progress + 1)
                    self.resize(int(self.allocSize * l))
                if self.used[begin]:
                    continue
                i = 1
                while i < len(siblings):
                    if self.ac.check[begin + siblings[i].keys()[0]] != 0:
                        flag = 1
                    if flag == 1:
                        break
                    i += 1
                if flag == 1:
                    continue

                break
            if 1.0 * nonzero_num / (pos - self.nextCheckPos + 1) >= 0.95:
                # 从位置 next_check_pos 开始到 pos 间，如果已占用的空间在95%以上，下次插入节点时，直接从 pos 位置处开始查找
                self.nextCheckPos = pos
            self.used[begin] = True
            if not self.ac.size > begin + siblings[len(siblings) - 1].keys()[0] + 1:
                self.ac.size = begin + siblings[len(siblings) - 1].keys()[0] + 1
            for sibling in siblings:
                self.ac.check[begin + sibling.keys()[0]] = begin
            for sibling in siblings:
                new_siblings = []
                if self.fetch(sibling.values()[0], new_siblings) == 0:
                    self.ac.base[begin + sibling.keys()[0]] = (-sibling.values()[0].getLargestValueId()) - 1
                    self.progress += 1
                else:
                    h = self.insert(new_siblings)
                    self.ac.base[begin + sibling.keys()[0]] = h
                sibling.values()[0].setIndex(begin + sibling.keys()[0])
            return begin

        def constructOutput(self, targetState):
            """
            建立output表
            :param targetState:
            :return:
            """
            emit = targetState.getEmit()
            if emit is None or len(emit) == 0:
                return
            output = [int()] * len(emit)
            it = iter(emit)
            for i in range(len(output)):
                output[i] = it.next()
            self.ac.output[targetState.getIndex()] = output

        def constructFailuresStates(self):
            """
            建立failure表
            :return:
            """
            self.ac.fail = [int()] * (self.ac.size + 1)
            self.ac.fail[1] = self.ac.base[0]
            self.ac.output = [None] * (self.ac.size + 1)

            queue = Queue.Queue()

            # 第一步，将深度为1的节点的failure设为根节点
            for depthOneState in self.rootState.getStates():
                depthOneState.setFailure(self.rootState, self.ac.fail)
                queue.put(depthOneState)
                self.constructOutput(depthOneState)
            # 第二步，为深度 > 1的节点建立failure表，这是一个bfs
            while not queue.empty():
                currentState = queue.get()
                for transition in currentState.getTransitions():
                    targetState = currentState.nextState(transition)
                    queue.put(targetState)

                    traceFailureState = currentState.getFailure()
                    while traceFailureState.nextState(transition) is None:
                        traceFailureState = traceFailureState.getFailure()

                    newFailureState = traceFailureState.nextState(transition)
                    targetState.setFailure(newFailureState, self.ac.fail)
                    targetState.addEmit1(newFailureState.getEmit())
                    self.constructOutput(targetState)

        def loseWeight(self):
            """
            释放空闲的内存
            :return:
            """
            nbase = [int()] * (self.ac.size + 65535)
            nbase[:self.ac.size] = self.ac.base[:self.ac.size]
            self.ac.base = nbase

            ncheck = [int()] * (self.ac.size + 65535)
            ncheck[:self.ac.size] = self.ac.check[:self.ac.size]
            self.ac.check = ncheck


# 跳出外层循环类
class Getoutofloop(Exception):
    pass


if __name__ == "__main__":
    ac = AhoCorasickDoubleArrayTrie()
    ac.Builder(ac).resize(9)
