# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-02

"""
 一个状态有如下几个功能
 success; 成功转移到另一个状态
 failure; 不可顺着字符串跳转的话，则跳转到一个浅一点的节点
 emits; 命中一个模式串
 根节点稍有不同，根节点没有 failure 功能，它的“failure”指的是按照字符串路径转移到下一个状态。其他节点则都有failure状态。
 @author lsd
"""
from collection.treemap.TreeMap import TreeMap


class State(object):
    def __init__(self):
        # 模式串的长度，也是这个状态的深度
        self.depth = int()
        # 只要这个状态可达，则记录模式串
        self.emits = None
        # goto 表，也称转移函数。根据字符串的下一个字符转移到下一个状态
        self.success = TreeMap({})
        # 在双数组中的对应下标
        self.index = int()
        # fail 函数，如果没有匹配到，则跳转到此状态。
        self.failure = None

    def init1(self, depth):
        """
        构造深度为depth的节点
        :param depth:
        :return:
        """
        self.depth = depth
        return self

    def isAcceptable(self):
        """
        是否是终止状态
        :return:
        """
        return self.depth > 0 and self.emits is not None

    def getDepth(self):
        """
        获取节点深度
        :return:
        """
        return self.depth

    def getLargestValueId(self):
        """
        获取最大的值
        :return:
        """
        if self.emits is None or len(self.emits) == 0:
            return None
        return iter(self.emits).next()

    def addEmit(self, keyword):
        """
        添加一个匹配到的模式串（这个状态对应着这个模式串)
        :param keyword:
        :return:
        """
        if self.emits is None:
            # self.emits是倒序排列的treeset
            # this.emits = new TreeSet<Integer>(Collections.reverseOrder());
            self.emits = set()
        self.emits = set(tuple(self.emits))
        self.emits.add(keyword)
        self.emits = sorted(self.emits, reverse=True)

    def addEmit1(self, emits):
        """
        添加一些匹配到的模式串
        :param emits:
        :return:
        """
        for emit in emits:
            self.addEmit(emit)

    def nextStateIgnoreRootState(self, character):
        return self.nextState1(character, True)

    def addState(self, character):
        character = character.encode('utf-8')
        nextState = self.nextStateIgnoreRootState(character)
        if nextState is None:
            nextState = State().init1(self.depth + 1)
            self.success.result[character] = nextState
            self.success = TreeMap(inputDict=self.success.result).sort()
        return nextState

    def getSuccess(self):
        """
        获取goto表
        :return:
        """
        return self.success

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def getStates(self):
        return self.success.values()

    def setFailure(self, failState, fail):
        """
        设置failure状态
        :param failState:
        :param fail:
        :return:
        """
        self.failure = failState
        fail[self.index] = failState.index

    def getEmit(self):
        """
        获取这个节点代表的模式串（们）
        :return:
        """
        if self.emits is None:
            return set()
        else:
            return self.emits

    def getTransitions(self):
        return set(self.success.keys())

    def nextState(self, character):
        """
        按照character转移，根节点转移失败会返回自己（永远不会返回null）
        :param character:
        :return:
        """
        return self.nextState1(character, False)

    def nextState1(self, character, ignoreRootState):
        """
        转移到下一个状态
        :param character:希望按此字符转移
        :param ignoreRootState:是否忽略根节点，如果是根节点自己调用则应该是true，否则为false
        :return:转移结果
        """
        nextState = self.success.get(character)
        if not ignoreRootState and nextState is None and self.depth == 0:
            nextState = self
        return nextState

    def getFailure(self):
        """
        获取failure状态
        :return:
        """
        return self.failure
