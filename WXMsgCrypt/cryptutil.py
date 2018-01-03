#!/usr/bin/env python
# coding=utf-8


def to_utf8_btyes(obj):
    """将 values 转为 bytes，默认编码 utf-8
    :param obj: 待转换的值
    """
    return obj.encode("utf-8")


def to_utf8_str(obj):
    """将 value 转为 unicode，默认编码 utf-8
    :param obj: 待转换的值
    """
    return obj.decode("utf-8")
