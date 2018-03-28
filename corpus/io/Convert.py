# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-23

class Convert:
    @staticmethod
    def convert(v):
        """
        将整数准换为16进制
        :param v: 
        :return: 
        """
        res = ''
        num = (v >> 24) & 0xFF
        num = hex(num)[2:].strip('L')
        res += '0' * (2 - len(num)) + num
        num = (v >> 16) & 0xFF
        num = hex(num)[2:].strip('L')
        res += '0' * (2 - len(num)) + num
        num = (v >> 8) & 0xFF
        num = hex(num)[2:].strip('L')
        res += '0' * (2 - len(num)) + num
        num = (v >> 0) & 0xFF
        num = hex(num)[2:].strip('L')
        res += '0' * (2 - len(num)) + num
        res = "%s %s\n" % (res[:4], res[4:])
        return res

    @staticmethod
    def convert_int(v):
        num_16 = ''
        if v >= 0:
            num = hex(v)
            num_16 = hex(v)[2:]
            num_16 = '0' * (8 - len(num_16)) + num_16
            num_16 = "%s %s\n" % (num_16[:4], num_16[4:])
        else:
            num_16 = hex(pow(16, 8) - int(abs(v)))[2:10]
            num_16 = "%s %s\n" % (num_16[:4], num_16[4:])
        return num_16

    @staticmethod
    def convert_char(v):
        res = ''
        num = (v >> 8) & 0xFF
        res += '0' * (2 - len(hex(num)[2:])) + hex(num)[2:]
        num = (v >> 0) & 0xFF
        res += '0' * (2 - len(hex(num)[2:])) + hex(num)[2:]
        res += "\n"
        return res

    @staticmethod
    def convert_byte(v):
        res = ''
        num = (v >> 0) & 0xFF
        res += '0' * (4 - len(hex(num)[2:])) + hex(num)[2:]
        res += "\n"
        return res


if __name__ == "__main__":
    print Convert.convert_char(ord('m'))
