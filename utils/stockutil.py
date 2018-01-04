#!/usr/bin/env python
# coding=utf-8


import json
from easyquotation import use

# 实例化新浪免费行情接口
sina_quotation = use("sina")


def summary_stock():
    # 上证指数，深证成指，创业板指
    acodes = ('sh000001', 'sz399001', 'sz399006')
    result = sina_quotation.stocks(list(acodes))
    summarystr = ''
    for key in result.keys():
        item = result[key]
        name = item['name']
        openvalue = item['open']
        now = item['now']
        jg = float('%.4f' % ((now - openvalue) / openvalue))
        if jg >= 0:
            ratio = '+' + str(jg*100.0) + '%'

        if summarystr:
            summarystr = summarystr + '\n' + name + ': ' + ratio + ', ' + str(openvalue) + ', ' + str(now)
        else:
            summarystr = name + ': ' + ratio + ', ' + str(openvalue) + ', ' + str(now)
    return summarystr


if __name__ == "__main__":
    print(summary_stock())
