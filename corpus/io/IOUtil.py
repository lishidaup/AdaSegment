# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-22
"""
一些常用的IO操作
"""
from Utility.Predefine import Predefine


class IOUtil(object):
    """
    序列化对象
    """

    def __init__(self):
        self.logger = Predefine.logger

    def readBytes(self, path):
        """
        将整个文件读取为字节数组
        :param path: 
        :return: 
        """

        try:
            return self.readBytesFromFile(path)
        except Exception, e:
            self.logger.warning("读取%s时发生异常%s" % (path, str(e)))
        
        return None


    def readBytesFromFile(self, path):
        bytes = []
        file1 = open(path, 'r')
        n = 1
        while 1:
            line = file1.readline().strip(' \r\n')
            if not line:
                break

            for item in line.split(' '):
                i1 = item[:2]
                i2 = item[2:]

                for i in [i1, i2]:
                    if i != '':
                        v = int(i, 16)
                        if v >= 128:
                            v = v - 256
                        bytes.append(v)
            n += 1
        return bytes


if __name__ == "__main__":
    IOUtil().readBytesFromFile("E:/pycharmprojects/AdaSegment/data/dictionary/person/nr.txt.value.dat")