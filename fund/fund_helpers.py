#!/usr/bin/env python
# coding=utf-8

import urllib3
import re
import datetime

pool = urllib3.PoolManager()


# 获取基金列表
def get_fund_codes(file_path):
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
    with open(file_path, 'wb') as f:
        f.write(result.encode('utf-8'))


if __name__ == "__main__":
    get_fund_codes("fund_codes.conf")
