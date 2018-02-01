#!/usr/bin/env python
# coding=utf-8

import json
from apscheduler.schedulers.background import BackgroundScheduler
from bottle import Bottle, run, request, template, response
from cron import taskjobs
from urllib import parse
from libs.bottleplugins.canister import Canister
from wx.wxapi import encrypt, decrypt, wx_account, extract
import time
from utils import stockutil
from fund import fund_rank, fund_helpers


app = Bottle()
bottle_config = app.config.load_config("config/app.conf")
app.install(Canister())


@app.route('/')
def index():
    # app.log.info("access web root index...")
    return "Welcome to python web!"


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
            s_content = fund_rank.fund_detail_openid(fromuser, "config/fund.json")
        elif req_content == 'stock':
            # 获取股票收益
            s_content = "=="
        else:
            # 获取当日大盘概况
            s_content = stockutil.summary_stock()
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
    # 启动时创建基金codes文件
    fund_helpers.get_fund_codes("fund/fund_codes.conf")
    with open("config/jobs.json", 'r') as f:
        conf = json.load(f)
    if "jobs" in conf:
        sched_jobs = conf["jobs"]
    sched = BackgroundScheduler()
    for job in sched_jobs:
        if job.pop("enable").lower() == "true":
            job["func"] = getattr(taskjobs, job["func"])
            sched.add_job(**job)
    # 启动定时任务
    add_jobs = sched.get_jobs()
    if add_jobs.__len__() > 0:
        sched.start()
    run(app, **bottle_config)
