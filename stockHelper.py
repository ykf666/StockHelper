#!/usr/bin/env python
# coding=utf-8

from bottle import Bottle, run, request, template, response, static_file
from urllib import parse
from libs.bottleplugins.canister import Canister
from libs.bottleplugins.boot import Boot
from wx.wxapi import encrypt, decrypt, wx_account, extract, check_signature
import time
from stock.stock_api import summary_stock, detail_stock, detail_stock_by_name
import re
from db.db_sqlite3 import add_user_stock


app = Bottle()
bottle_config = app.config.load_config("config/app.conf")
app.install(Canister())
app.install(Boot())
SETUP_BASE_URL = "http://wx.gxm.cloudns.asia/html/stock_setup.html?uid="
logger = app.log


# @app.route('/', method="GET")
# def index():
#     # 读取url参数
#     qs = parse.parse_qs(request.query_string)
#     req_str = qs["test"][0]
#     if req_str == 'stock':
#         s_content = detail_stock('600903')
#     elif re.match('^(?=.*[\u4E00-\u9FA5])[A-Z\u4E00-\u9FA5]*$', "ST宜化"):
#         s_content = detail_stock_by_name("*ST宜化")
#     return s_content


@app.route('/', method="GET")
def hello():
    app.log.info(request.query_string)
    response.content_type = 'application/xml; charset=utf-8'
    # 读取url参数
    qs = parse.parse_qs(request.query_string)
    signature = qs["signature"][0]
    timestamp = qs["timestamp"][0]
    nonce = qs["nonce"][0]
    echostr = qs["echostr"][0]
    app.log.info("Request signature: %s" % signature)
    if check_signature(signature, timestamp, nonce):
        return echostr
    else:
        return "fail"


@app.route('/', method="POST")
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
        elif re.match('^(?=.*[\u4E00-\u9FA5])[A-Z\u4E00-\u9FA5]*$', req_content):
            s_content = detail_stock_by_name(req_content)
        else:
            # 获取当日大盘概况
            s_content = summary_stock(fromuser)
    elif msgtype == "event":
        eventtype = extract(decrypt_xml, "Event")
        if eventtype == "subscribe":
            s_content = "欢迎您，感谢订阅股小秘，回复任意文本消息，获取股市行情。如需自定义股票，请回复'setup'指令。"
        else:
            s_content = "success"
    else:
        s_content = "开发中，敬请期待！"

    setup_url = SETUP_BASE_URL + fromuser
    if req_content == 'setup':
        s_xml = template('send_news', touser=fromuser, fromuser=wx_account, createtime=int(time.time()),
                         setupurl=setup_url)
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
    try:
        # 读取post数据
        req_data = request.body.read().decode()
        qs = parse.parse_qs(req_data)
        stock_code = qs["code"][0]
        openid = qs["uid"][0]
        logger.info('user %s set stock: %s' % (openid, stock_code))
        return add_user_stock(openid, stock_code)
    except RuntimeError:
        return '{"code":-1,"result":"失败"}'


if __name__ == '__main__':
    run(app, **bottle_config)
