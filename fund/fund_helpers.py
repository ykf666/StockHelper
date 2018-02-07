#!/usr/bin/env python
# coding=utf-8

import urllib3
import os
import re


FUND_CODE_PATH = 'fund_codes.conf'
pool = urllib3.PoolManager()


# 获取基金列表
def get_fund_codes():
    result = ''
    data_re = re.compile(r'=.\[(.*?)\];$')
    item_re = re.compile(r'\[(.*?)\]')
    # today = datetime.datetime.now().strftime('%Y-%m-%d')
    r_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    res_data = pool.request('GET', r_url).data.decode('utf-8')
    for line in data_re.findall(res_data):
        if line != "":
            for line2 in item_re.findall(line):
                item_list = line2.split(',')
                if result == "":
                    result = result + item_list[0] + ":" + item_list[2]
                else:
                    result = result + "," + item_list[0] + ":" + item_list[2]
    result = "{" + result + "}"
    with open(fund_code_path(), 'wb') as f:
        f.write(result.encode("utf-8"))


def fund_code_path():
    return os.path.join(os.path.dirname(__file__), FUND_CODE_PATH)


if __name__ == "__main__":
    get_fund_codes()
