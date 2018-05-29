#!/usr/bin/env python
# coding=utf-8

from bottle import Bottle, run, request, template, response, static_file
from urllib import parse
from libs.bottleplugins.canister import Canister
from libs.bottleplugins.boot import Boot
from wx.wxapi import encrypt, decrypt, wx_account, extract
import time
from stock.stock_api import summary_stock, detail_stock
import re

app = Bottle()
bottle_config = app.config.load_config("config/app.conf")
app.install(Canister())
app.install(Boot())


@app.route('/', method="GET")
def index():
    # 读取url参数
    qs = parse.parse_qs(request.query_string)
    req_str = qs["test"][0]
    if req_str == 'stock':
        s_content = detail_stock('600903')
    else:
        s_content = summary_stock()
    return s_content


@app.route('/wx', method="POST")
def wx():
    response.content_type = 'application/xml; charset=utf-8'
    # 读取url参数
    qs = parse.parse_qs(request.query_string)
    signature = qs["signature"][0]
    timestamp = qs["timestamp"][0]
    nonce = qs["nonce"][0]
    msg_signature = qs["msg_signature"][0]
    app.log.info("Request signature: %s" % signature)
    # 读取post数据
    from_xml = request.body.read().decode()
    # 接收消息解密
    ret, decrypt_xml = decrypt(from_xml, msg_signature, timestamp, nonce)
    app.log.info("Request xml: %s" % decrypt_xml)

    msgtype = extract(decrypt_xml, "MsgType")
    fromuser = extract(decrypt_xml, "FromUserName")
    if msgtype == "text":
        req_content = extract(decrypt_xml, "Content")
        if re.match('[0-9]{6}', req_content):
            # 根据股票代码查询个股详情
            s_content = detail_stock(req_content)
        else:
            # 获取当日大盘概况
            s_content = summary_stock()
    elif msgtype == "event":
        eventtype = extract(decrypt_xml, "Event")
        if eventtype == "subscribe":
            s_content = "欢迎您，感谢订阅股小秘，回复任意文本消息，获取股市行情。如需帮助，请回复'help'指令。"
        else:
            s_content = "success"
    else:
        s_content = "开发中，敬请期待！"

    if req_content == 'help':
        s_xml = template('send_news', touser=fromuser, fromuser=wx_account, createtime=int(time.time()))
    else:
        s_xml = template('send_msg', touser=fromuser, fromuser=wx_account, createtime=int(time.time()),
                         content=s_content)
    app.log.info("Response xml: %s" % s_xml)
    # 加密返回消息字符串
    ret, to_xml = encrypt(s_xml, nonce)
    return to_xml


@app.route('/html/<path>')
def html(path):
    return static_file(path, root='views')


@app.route('/api/stock/setup', method="POST")
def stock_add():
    # 读取post数据
    req_data = request.body.read().decode()
    qs = parse.parse_qs(req_data)
    stock_code = qs["code"][0]
    openid = qs["openid"][0]
    print(qs["code"][0])
    return '{"code":0,"result":"成功"}'


if __name__ == '__main__':
    run(app, **bottle_config)
