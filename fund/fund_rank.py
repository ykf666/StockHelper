#!/usr/bin/env python
# coding=utf-8

import urllib3
import re
import datetime
import json

datefmt = '%Y-%m-%d'
pool = urllib3.PoolManager()
base_url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz'
today = datetime.datetime.now()

fund_dict = {}
try:
    with open('fund_codes.conf', 'r', encoding='utf-8') as f:
        fund_dict = eval(f.read())
except IOError:
    print(IOError.strerror)
else:
    f.close()


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


# 根据openid获取基金收益详情
def fund_detail_openid(open_id, file_path):
    with open(file_path, encoding='utf-8') as f:
        conf = json.load(f)
    result = ''
    if open_id in conf:
        for u_conf in conf[open_id]:
            code = u_conf['code']
            cost_price = u_conf['cost_price']
            count = u_conf['count']
            res = get_fund_price(code)
            print(res)
            current_price = float(res[1])

            fund_name = fund_dict[code]
            # 单位净值差额(当前价格-成本价)
            difference = current_price - cost_price
            jg = float('%.4f' % (difference / cost_price))
            ratio = '+' if jg >= 0 else ''
            ratio = ratio + str('%.2f' % (jg * 100.00)) + '%'
            cysy = float('%.2f' % (count * difference))
            if result:
                result = result + '\n' + fund_name + ': ' + ratio + ', ' + str(cysy)
            else:
                result = fund_name + ': ' + ratio + ', ' + str(cysy)
        return result
    else:
        return "您目前没有配置基金购买情况，无法获取收益详情！"


if __name__ == "__main__":
    print(fund_detail_openid("oBBGPwGoZ4mM0u4oP_jkXKvdTtYc"))
