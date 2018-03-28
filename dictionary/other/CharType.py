# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-27

"""
字符类型
"""
from Utility.TextUtility import TextUtility
from Utility.Predefine import Predefine
from corpus.io.ByteArray import ByteArray
from corpus.io.Convert import Convert
from Config import Config
from time import time
import cPickle
import sys


class CharType(object):
    type = []
    CT_SINGLE = 5
    # 分隔符"!,.?()[]{}+=
    CT_DELIMITER = CT_SINGLE + 1
    # 中文字符
    CT_CHINESE = CT_SINGLE + 2
    # 字母
    CT_LETTER = CT_SINGLE + 3
    # 数字
    CT_NUM = CT_SINGLE + 4
    # 序号
    CT_INDEX = CT_SINGLE + 5
    # 其他
    CT_OTHER = CT_SINGLE + 12

    def __init__(self):
        # 单字节
        self.logger = Predefine.logger
        self.init()

    def init(self):
        CharType.type = [bytes()] * 65536
        self.logger.info("字符类型对应表开始加载" + Config.CharTypePath)
        start = time()
        try:
            byteArray = cPickle.load(open(Config.CharTypePath, 'rb'))
        except Exception, e:
            byteArray = ByteArray.createByteArray(Config.CharTypePath)
            out = file(Config.CharTypePath + Predefine.PIC_EXT, 'wb')
            cPickle.dump(byteArray, out)
        if byteArray is None:
            try:
                byteArray = CharType.generate()
            except Exception, e:
                self.logger.error("字符类型对应表%s加载失败" % Config.CharTypePath)
                sys.exit(1)
        while byteArray.hasMore():
            b = byteArray.nextChar()
            e = byteArray.nextChar()
            t = byteArray.nextByte()
            for i in range(b, e + 1):
                self.type[i] = t
        self.logger.info("字符类型对应表加载成功，耗时%fms" % (time() - start) * 1000)
        print "字符类型对应表%s加载成功，耗时%fms" % (Config.CharTypePath, (time() - start) * 1000)

    @staticmethod
    def generate():
        preType = 5
        preChar = 0
        typeList = []
        for i in range(65535):
            type = TextUtility.charType(i)
            if type != preType:
                array = [int()] * 3
                array[0] = preChar
                array[1] = i - 1
                array[2] = preType
                typeList.append(array)
            preChar = i
        array = [int()] * 3
        array[0] = preChar
        array[1] = 65535
        array[2] = preType
        typeList.append(array)
        out = file(Config.CharTypePath, 'w+')
        for array in typeList:
            out.writelines(Convert.convert_char(array[0]))
            out.writelines(Convert.convert_char(array[1]))
            out.writelines(Convert.convert_byte(array[2]))
        out.close()
        byteArray = ByteArray.createByteArray(Config.CharTypePath)
        return byteArray

    @staticmethod
    def get(c):
        """
        获取字符的类型
        :param c:
        :param ct_obj:
        :return:
        """
        return CharType.type[ord(c)]


if __name__ == '__main__':
    CharType()
