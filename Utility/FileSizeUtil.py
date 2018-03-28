# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-15
"""
获取文件大小
"""
import os
import numpy as np


class FileSizeUtil(object):
    @staticmethod
    def formatSize(bytes_in):
        bytes_size = float(bytes_in)
        return bytes_size

    @staticmethod
    def getFileSize(path):
        size = os.path.getsize(path)
        return FileSizeUtil.formatSize(size)

    @staticmethod
    def readFile(path):
        res = []
        size = FileSizeUtil.getFileSize(path)
        f = open(path, 'r')
        for i in range(int(size)):
            char = f.read(1)
            if char != '':
                asi = ord(char)
                res.append(asi)
            else:
                break
        f.close()
        return res


if __name__ == "__main__":
    FileSizeUtil.readFile("E:/pycharmprojects/IfengNLP/data/dictionary/person/nr.txt.trie.dat")
