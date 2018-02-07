#!/usr/bin/env python
# coding=utf-8

from bottle import Bottle, run, request, template, response
from urllib import parse
from libs.bottleplugins.canister import Canister
from libs.bottleplugins.boot import Boot
from wx.wxapi import encrypt, decrypt, wx_account, extract
import time
from stock.stock_api import summary_stock
from fund.fund_api import fund_detail_openid


app = Bottle()
bottle_config = app.config.load_config("config/app.conf")
app.install(Canister())
app.install(Boot())


@app.route('/', method="GET")
def index():
    print(request.params)
    # 读取url参数
    qs = parse.parse_qs(request.query_string)
    req_str = qs["test"][0]
    if req_str == 'fund':
        s_content = fund_detail_openid("oBBGPwGoZ4mM0u4oP_jkXKvdTtYc")
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
        if req_content == 'fund':
            # 获取基金收益
            s_content = fund_detail_openid(fromuser)
        elif req_content == 'stock':
            # 获取股票收益
            s_content = "=="
        else:
            # 获取当日大盘概况
            s_content = summary_stock()
    elif msgtype == "event":
        eventtype = extract(decrypt_xml, "Event")
        if eventtype == "subscribe":
            s_content = "欢迎您，感谢订阅股小秘，回复任意文本消息，获取股市行情。"
        else:
            s_content = "success"
    else:
        s_content = "开发中，敬请期待！"

    s_xml = template('send_msg', touser=fromuser, fromuser=wx_account, createtime=int(time.time()), content=s_content)
    app.log.info("Response xml: %s" % s_xml)
    # 加密返回消息字符串
    ret, to_xml = encrypt(s_xml, nonce)
    return to_xml


if __name__ == '__main__':
    run(app, **bottle_config)
