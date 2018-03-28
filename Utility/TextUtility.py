# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-06-09

"""
文本工具类
"""


class TextUtility(object):
    # 单字节
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
        pass

    @staticmethod
    def charType(c):
        return TextUtility.charType1(str(c))

    @staticmethod
    def charType1(str):
        if str is not None and len(str) > 0:
            if str in "零○〇一二两三四五六七八九十廿百千万亿壹贰叁肆伍陆柒捌玖拾佰仟":
                return TextUtility.CT_NUM
            b = []
            try:
                b = bytearray(str.encode(encoding='gb2312'))
            except Exception, e:
                b = bytearray(str)
            b1 = b[0]
            if len(b) > 1:
                b2 = b[1]
            else:
                b2 = 0
            ub1 = TextUtility.getUnsigned(b1)
            ub2 = TextUtility.getUnsigned(b2)
            if ub1 < 128:
                if ' ' == b1:
                    return TextUtility.CT_OTHER
                if '\n' == b1:
                    return TextUtility.CT_DELIMITER
                b1 = b.decode()[0]
                if "*\"!,.?()[]{}+=/\\;:|".index(b1) != -1:
                    return TextUtility.CT_DELIMITER
                if "0123456789".index(b1) != -1:
                    return TextUtility.CT_NUM
                return TextUtility.CT_SINGLE
            elif ub1 == 162:
                return TextUtility.CT_INDEX
            elif ub1 == 163 and 175 < ub2 < 186:
                return TextUtility.CT_NUM
            elif ub1 == 163 and ((193 <= ub2 <= 218) or (225 <= ub2 <= 250)):
                return TextUtility.CT_LETTER
            elif ub1 == 161 or ub1 == 163:
                return TextUtility.CT_DELIMITER
            elif 176 <= ub1 <= 247:
                return TextUtility.CT_CHINESE
        return TextUtility.CT_OTHER

    @staticmethod
    def getUnsigned(b):
        if b > 0:
            return int(b)
        else:
            return b & 0x7F + 128
