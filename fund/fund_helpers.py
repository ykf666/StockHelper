#!/usr/bin/env python
# coding=utf-8

import urllib3
import re
from utils.db_mongo import add_fund_info, fund_set_count, update_fund_info


pool = urllib3.PoolManager()


# 初始化基金信息
def init_fund_infos():
    data_re = re.compile(r'=.\[(.*?)\];$')
    item_re = re.compile(r'\[(.*?)\]')
    # today = datetime.datetime.now().strftime('%Y-%m-%d')
    r_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    res_data = pool.request('GET', r_url).data.decode('utf-8')
    for line in data_re.findall(res_data):
        if line != "":
            for line2 in item_re.findall(line):
                item_list = line2.split(',')
                fund_code = item_list[0]
                fund_name = item_list[2]
                add_fund_info(fund_code, fund_name)


# 更新基金信息
def update_fund_infos():
    if fund_set_count() == 0:
        init_fund_infos()
    else:
        data_re = re.compile(r'=.\[(.*?)\];$')
        item_re = re.compile(r'\[(.*?)\]')
        # today = datetime.datetime.now().strftime('%Y-%m-%d')
        r_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
        res_data = pool.request('GET', r_url).data.decode('utf-8')
        for line in data_re.findall(res_data):
            if line != "":
                for line2 in item_re.findall(line):
                    item_list = line2.split(',')
                    fund_code = item_list[0]
                    fund_name = item_list[2]
                    update_fund_info(fund_code, fund_name)


if __name__ == "__main__":
    update_fund_infos()
