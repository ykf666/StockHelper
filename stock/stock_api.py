#!/usr/bin/env python
# coding=utf-8

from libs.easyquotation import use

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
        close_yesterday = item['close']
        now = item['now']
        jg = float('%.4f' % ((now - close_yesterday) / close_yesterday))
        ratio = '+' if jg >= 0 else ''
        ratio = ratio + str('%.2f' % (jg*100.00)) + '%'
        if summarystr:
            summarystr = summarystr + '\n' + name + ': ' + ratio + ', ' + str(float('%.2f' % now))
        else:
            summarystr = name + ': ' + ratio + ', ' + str(float('%.2f' % now))
    return summarystr


if __name__ == "__main__":
    print(summary_stock())
