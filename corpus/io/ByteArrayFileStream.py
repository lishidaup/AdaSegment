# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-15
"""
流式的字节数组，降低读取时的内存峰值
"""
from corpus.io.ByteArrayStream import ByteArrayStream
from Utility.Predefine import Predefine
from Utility.FileSizeUtil import FileSizeUtil


class ByteArrayFileStream(ByteArrayStream):
    logger = Predefine.logger

    def __init__(self):
        ByteArrayStream.__init__(self)

    def init2(self, bytes, bufferSize):
        self.init1(bytes, bufferSize)
        return self

    @staticmethod
    def createByteArrayFileStream(path):
        try:
            f = open(path, 'r')
            size = FileSizeUtil.getFileSize(path)
            bufferSize = int(min(1048576, size))
            bytes_arr = []
            return ByteArrayFileStream().init1(bytes_arr, bufferSize)
        except Exception, e:
            ByteArrayFileStream.logger = Predefine.logger
            return None
