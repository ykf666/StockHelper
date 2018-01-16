#!/usr/bin/env python
# coding=utf-8

import urllib3
import re

pool = urllib3.PoolManager()

if __name__ == "__main__":
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + '110026' \
          + '&page=1&per=20&sdate=' + '2018-01-10' + '&edate=' + '2018-01-12'
    response = pool.request('GET', url)
    resp_data = response.data.decode('utf-8')
    print(resp_data)

    tr_re = re.compile(r'<tr>(.*?)</tr>')
    item_re = re.compile(r'''<td>(\d{4}-\d{2}-\d{2})</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>
                        (.*?)</td><td.*?>(.*?)</td><td.*?></td>''', re.X)
    for line in tr_re.findall(resp_data):
        match = item_re.match(line)
        if match:
            entry = match.groups()
            print(entry[0] + ", " + entry[1])
