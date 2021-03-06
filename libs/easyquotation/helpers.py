# coding:utf8
import json
import os
import re

import requests
from db.db_sqlite3 import count_stock_set, clear_stock_set, batch_insert_stock_info


STOCK_CODE_PATH = 'stock_codes.conf'
REQUEST_URL = 'http://www.shdjt.com/js/lib/astock.js'


def update_stock_codes():
    """获取所有股票 ID 到 all_stock_code 目录下"""
    grep_stock_codes = re.compile('~(\d+)`')
    response = requests.get(REQUEST_URL)
    all_stock_codes = grep_stock_codes.findall(response.text)
    with open(stock_code_path(), 'w') as f:
        f.write(json.dumps(dict(stock=all_stock_codes)))


def get_stock_codes(realtime=False):
    """获取所有股票 ID 到 all_stock_code 目录下"""
    if realtime:
        grep_stock_codes = re.compile('~(\d+)`')
        response = requests.get(REQUEST_URL)
        stock_codes = grep_stock_codes.findall(response.text)
        with open(stock_code_path(), 'w') as f:
            f.write(json.dumps(dict(stock=stock_codes)))
        return stock_codes
    else:
        with open(stock_code_path()) as f:
            return json.load(f)['stock']


def stock_code_path():
    return os.path.join(os.path.dirname(__file__), STOCK_CODE_PATH)


# mongodb初始化股票code及name
# def init_stock_infos():
#     grep_stock_codes = re.compile('~(\d+)(\D+)`')
#     response = requests.get(REQUEST_URL)
#     stock_infos = grep_stock_codes.findall(response.text)
#     for stock in stock_infos:
#         code = stock[0]
#         name = stock[1].replace("`", "")
#         add_stock_info(code, name)


# mongodb更新股票code及name
# def update_stock_infos():
#     if stock_set_count() == 0:
#         init_stock_infos()
#     else:
#         grep_stock_codes = re.compile('~(\d+)(\D+)`')
#         response = requests.get(REQUEST_URL)
#         stock_infos = grep_stock_codes.findall(response.text)
#         for stock in stock_infos:
#             code = stock[0]
#             name = stock[1].replace("`", "")
#             update_stock_info(code, name)


# sqlite3初始化股票code及name
def init_stock_info_sqlite3():
        grep_stock_codes = re.compile('~(\d+)(\D+)`')
        response = requests.get(REQUEST_URL)
        stock_infos = grep_stock_codes.findall(response.text)
        data = []
        for stock in stock_infos:
            code = stock[0]
            name = stock[1].replace("`", "")
            item = (code, name)
            data.append(item)
        batch_insert_stock_info(data)


# sqlite3更新股票code及name
def update_stock_info_sqlite3():
    if count_stock_set() > 0:
        clear_stock_set()
    init_stock_info_sqlite3()


if __name__ == "__main__":
    init_stock_info_sqlite3()

