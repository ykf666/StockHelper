#!/usr/bin/env python
# coding=utf-8

import urllib3
import re
import datetime
import json

datefmt = '%Y-%m-%d'
pool = urllib3.PoolManager()
base_url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz'


def get_fund_price(code):
    to_date = datetime.datetime.now()
    from_date = to_date + datetime.timedelta(days=-10)
    r_url = base_url + '&code=' + code + '&page=1&per=20&sdate=' + from_date.strftime(datefmt) \
            + '&edate=' + to_date.strftime(datefmt)
    response = pool.request('GET', r_url)
    resp_data = response.data.decode('utf-8')
    print(resp_data)

    tr_re = re.compile(r'<tr>(.*?)</tr>')
    item_re = re.compile(r'''<td>(\d{4}-\d{2}-\d{2})</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>
                        (.*?)</td><td.*?>(.*?)</td><td.*?></td>''', re.X)
    for line in tr_re.findall(resp_data):
        match = item_re.match(line)
        if match:
            entry = match.groups()
            break
    return entry


if __name__ == "__main__":
    with open("../config/fund.json", 'r') as f:
        conf = json.load(f)
    if 'oBBGPwGoZ4mM0u4oP_jkXKvdTtYc' in conf:
        for u_conf in conf['oBBGPwGoZ4mM0u4oP_jkXKvdTtYc']:
            code = u_conf['code']
            cost_price = u_conf['cost_price']
            count = u_conf['count']
            name = u_conf['name']
            res = get_fund_price(code)
            print(res)
            current_price = float(res[1])
            ratio = float('%.4f' % ((current_price - cost_price) / cost_price))
            print(ratio)