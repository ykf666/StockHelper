#!/usr/bin/env python
# coding=utf-8

from libs.easyquotation import use

# 实例化新浪免费行情接口
sina_quotation = use("sina")


def summary_stock():
    # 上证指数，深证成指，创业板指，老板电器，福耀玻璃
    acodes = ('sh000001', 'sz399001', 'sz399006', '002508', '600660')
    result = sina_quotation.stocks(list(acodes))
    summarystr = ''
    line = 0
    for key in result.keys():
        item = result[key]

        name = item['name']
        close_yesterday = item['close']
        now = item['now']
        jg = float('%.4f' % ((now - close_yesterday) / close_yesterday))
        ratio = '+' if jg >= 0 else ''
        ratio = ratio + str('%.2f' % (jg * 100.00)) + '%'
        if summarystr:
            summarystr = summarystr + '\n' + name + ': ' + ratio + ', ' + str(float('%.2f' % now))
        else:
            summarystr = name + ': ' + ratio + ', ' + str(float('%.2f' % now))
        if line == 2:
            summarystr = summarystr + "\n===================="
        line = line + 1
    return summarystr


def detail_stock(stock_code):
    result = sina_quotation.real(stock_code)
    print(result)
    summarystr = ''
    item = result[stock_code]
    name = item['name']
    close_yesterday = item['close']
    now = item['now']
    jg = float('%.4f' % ((now - close_yesterday) / close_yesterday))
    ratio = '+' if jg >= 0 else ''
    ratio = ratio + str('%.2f' % (jg * 100.00)) + '%'
    if summarystr:
        summarystr = summarystr + '\n' + name + ': ' + ratio + ', ' + str(float('%.2f' % now))
    else:
        summarystr = name + ': ' + ratio + ', ' + str(float('%.2f' % now))
    return summarystr


if __name__ == "__main__":
    print(summary_stock())
