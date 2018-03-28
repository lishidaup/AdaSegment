# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-02

from Utility.Predefine import Predefine


class Config:
    # root = os.path.abspath(os.curdir)
    root = Predefine.ROOT
    root = root.replace('\\', '/')
    if not root.endswith('/'):
        root += '/'
    # 开发模式
    DEBUG = False
    # 核心词典路径
    CoreDictionaryPath = root + "dictionary/CoreNatureDictionary.txt"
    # 核心词典词性转移矩阵路径
    CoreDictionaryTransformMatrixDictionaryPath = root + "dictionary/CoreNatureDictionary.tr.txt"
    # 用户自定义词典路径
    CustomDictionaryPath = [root + "dictionary/custom/CustomDictionary.txt"]
    # 二元语法词典路径
    BiGramDictionaryPath = root + "dictionary/CoreNatureDictionary.ngram.txt"
    # 人名词典路径
    PersonDictionaryPath = root + "dictionary/person/nr.txt"
    # 人名词典转移矩阵路径
    PersonDictionaryTrPath = root + "dictionary/person/nr.tr.txt"
    # 地名词典路径
    PlaceDictionaryPath = root + "dictionary/place/ns.txt"
    # 地名词典转移矩阵路径
    PlaceDictionaryTrPath = root + "dictionary/place/ns.tr.txt"
    # 音译人名词典
    TranslatedPersonDictionaryPath = root + "dictionary/person/nrf.txt"
    # 日本人名词典路径
    JapanesePersonDictionaryPath = root + "dictionary/person/nrj.txt"
    # 机构名词典路径
    OrganizationDictionaryPath = root + "dictionary/organization/nt.txt"
    # 机构名词典转移矩阵路径
    OrganizationDictionaryTrPath = root + "dictionary/organization/nt.tr.txt"
    # 字符类型对应表
    CharTypePath = root + "dictionary/other/CharType.bin.txt"
    # 拼音词典路径
    PinyinDictionaryPath = "data/dictionary/pinyin/pinyin.txt"
    # 分词结果是否展示词性
    ShowTermNature = True

    def __init__(self):
        pass
