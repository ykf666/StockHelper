#!/usr/bin/env python
# coding=utf-8

from wx.wxapi import get_access_token
from requests import post
import json

create_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='


# 创建菜单，企业认证过的订阅号才有权限
def create_menu():
    url = create_url + get_access_token()
    with open("wx_menu.json", encoding='utf-8') as f:
        data = json.load(f)
    resp = post(url, data)
    print(resp.json())


if __name__ == '__main__':
    create_menu()
