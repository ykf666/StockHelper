#!/usr/bin/env python
# coding=utf-8

from libs.easyquotation import use
from utils.db_mongo import find_stocks_user, get_stock_code_by_name


# 实例化新浪免费行情接口
sina_quotation = use("sina")


def summary_stock(openid):
    # 上证指数，深证成指，创业板指
    acodes_base = ("sh000001", "sz399001", "sz399006")
    user_stock = find_stocks_user(openid)
    if user_stock is not None:
        stocks = user_stock["stock_codes"]
        acodes_ext = tuple(stocks.split(","))
        acodes = acodes_base + acodes_ext
    else:
        acodes = acodes_base
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
        if line == 3:
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


# 根据股票名称查询
def detail_stock_by_name(stock_name):
    result = get_stock_code_by_name(stock_name)
    if result is not None:
        return detail_stock(result)
    else:
        return "未查询到股票信息，请检查股票名称!"


if __name__ == "__main__":
    print(summary_stock())
