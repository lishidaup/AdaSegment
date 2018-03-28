# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-11


"""
分词器配置项
"""


class Config(object):
    def __init__(self):
        # 是否识别中国人名
        self.nameRecognize = True
        # 是否识别音译人名
        self.translateNameRecognize = True
        # 是否识别日本人名
        self.japaneseNameRecognize = True
        # 是否识别地名
        self.placeRecognize = True
        # 是否识别机构名
        self.organizationRecognize = True
        # 是否词性标注
        self.speechTagging = False
        # 命名实体识别是否至少有一项被激活
        self.ner = True
        # 是否计算偏移量
        self.offset = False
        # 分词结果是否展示词性
        self.ShowTermNature = True

    # 更新命名实体识别总开关
    def updateNerConfig(self):
        self.ner = self.nameRecognize or self.translateNameRecognize or self.japaneseNameRecognize or self.placeRecognize or self.organizationRecognize


if __name__ == "__main__":
    config = Config()
    config.updateNerConfig()
