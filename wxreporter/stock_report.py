#!/usr/bin/env python
# coding=utf-8

import json
from easyquotation import use

# 实例化新浪免费行情接口
sina_quotation = use("sina")

# 上证指数，深证成指，创业板指
composite_Index = ('sh000001', 'sz399001', 'sz399006')


def summary_stock():
    return sina_quotation.stocks(list(composite_Index))


def total_report():
    real_data = sina_quotation.stocks(list(composite_Index))
    for key in real_data.keys():
        stock_detail = real_data[key]
        print(stock_detail)
    return real_data



