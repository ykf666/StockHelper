#!/usr/bin/env python
# coding=utf-8

import urllib3
import os
import re
import datetime
import json
from pathlib import Path
from utils.logutil import getlogger

base_url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz'
datefmt = '%Y-%m-%d'
today = datetime.datetime.now()
current_dir = Path(__file__).parent
user_fund_dir = current_dir / 'user_fund'

pool = urllib3.PoolManager()
log = getlogger()


# 根据openid获取基金收益详情
def fund_detail_openid(open_id):
    if not user_fund_dir.exists():
        user_fund_dir.mkdir()
        log.info("create dirctory " + user_fund_dir.name)
    with open(str(current_dir / 'fund_codes.conf'), 'r', encoding='utf-8') as f:
        fund_dict = eval(f.read())
    with open(os.path.join(str(user_fund_dir), open_id), encoding='utf-8') as f:
        conf = json.load(f)
    result = ''
    for u_conf in conf:
        fcode = u_conf['code']
        cost_price = u_conf['cost_price']
        count = u_conf['count']
        res = get_fund_price(fcode)
        lastest_date = res[0]
        current_price = float(res[1])

        fund_name = fund_dict[fcode]
        # 单位净值差额(当前价格-成本价)
        difference = current_price - cost_price
        jg = float('%.4f' % (difference / cost_price))
        ratio = '+' if jg >= 0 else ''
        ratio = ratio + str('%.2f' % (jg * 100.00)) + '%'
        # 持有收益
        cysy = float('%.2f' % (count * difference))
        cysy_str = '+' if cysy >= 0 else ''
        cysy_str = cysy_str + str('%.2f' % cysy)
        if result:
            result = result + '\n' + "[" + lastest_date + "]" + fund_name + ': ' + ratio + ', ' + cysy_str
        else:
            result = "[" + lastest_date + "]" + fund_name + ': ' + ratio + ', ' + cysy_str
    return result
    # else:
    #     return "您目前没有配置基金购买情况，无法获取收益详情！"


# 查询基金详情
def get_fund_price(fund_code):
    from_date = datetime.datetime.now() + datetime.timedelta(days=-10)
    r_url = base_url + '&code=' + fund_code + '&page=1&per=20&sdate=' + from_date.strftime(datefmt) \
            + '&edate=' + today.strftime(datefmt)
    response = pool.request('GET', r_url)
    resp_data = response.data.decode('utf-8')

    tr_re = re.compile(r'<tr>(.*?)</tr>')
    item_re = re.compile(r'''<td>(\d{4}-\d{2}-\d{2})</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>
                        (.*?)</td><td.*?>(.*?)</td><td.*?></td>''', re.X)
    for line in tr_re.findall(resp_data):
        match = item_re.match(line)
        if match:
            entry = match.groups()
            break
    return entry


def set_fund_info(fund_code, cost_price, fund_count):
    with open(str(current_dir / 'fund_codes.conf'), 'r', encoding='utf-8') as f:
        fund_dict = eval(f.read())
    fund_name = fund_dict[fund_code]
    if fund_name == '':
        return "fail"
    data = '{name}'


if __name__ == "__main__":
    print(fund_detail_openid("oBBGPwGoZ4mM0u4oP_jkXKvdTtYc"))
