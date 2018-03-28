# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-23


class ByteUtil(object):
    @staticmethod
    def bytesHighFirstToInt(bytes, start):
        """
        字节数组和整型的转换，高位在前，适用于读取writeInt的数据
        :param bytes: 字节数组
        :param start: 
        :return: 整型
        """
        num = bytes[start + 3] & 0xFF
        num |= (bytes[start + 2] << 8) & 0xFF00
        num |= (bytes[start + 1] << 16) & 0xFF0000
        num |= (bytes[start] << 24) & 0xFF000000
        if (bytes[start] << 24) == -16777216:
            num |= -16777216
            return num
        num |= (bytes[start] << 24) & 0xFF000000
        return num

    @staticmethod
    def bytesHighFirstToChar(bytes, start):
        """
        字节数组转char，高位在前
        :param bytes:
        :param start:
        :return:
        """
        c = (bytes[start] & 0xFF) << 8 | (bytes[start + 1] & 0xFF)
        return c


if __name__ == "__main__":
    b = [-1, -1, -78, 58]
    print ByteUtil.bytesHighFirstToInt(b, 0)
    print ByteUtil.bytesHighFirstToChar(b, 0)
