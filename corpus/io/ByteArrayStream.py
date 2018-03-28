# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-14


from corpus.io.ByteArray import ByteArray
from corpus.io.ByteArrayFileStream import ByteArrayFileStream
from abc import ABCMeta, abstractmethod


class ByteArrayStream(ByteArray):
    __metaclass__ = ABCMeta

    def __init__(self):
        ByteArray.__init__(self)
        self.bufferSize = int()

    def init1(self, bytes, bufferSize):
        self.init(bytes)
        self.bufferSize = bufferSize

    @staticmethod
    def createByteArrayStream(path):
        pass

    @staticmethod
    def createByteArrayFileStream(path):
        try:
            f = open(path, 'r')
            return ByteArrayStream.createByteArrayFileStream1(f)
        except Exception, e:
            pass

    @staticmethod
    def createByteArrayFileStream1(f):
        pass
