#!/usr/bin/env python
# coding=utf-8

import json
from apscheduler.schedulers.background import BackgroundScheduler
from bottle import Bottle, run, request, template, response
from cron import taskjobs
from urllib import parse
from bottleplugins.canister import Canister
from wx.wxapi import encrypt, decrypt, wx_account, get_msg_id, get_random_str, extract
import time

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
    openid = qs["openid"][0]
    msg_signature = qs["msg_signature"][0]
    app.log.info("Signature: %s" % signature)
    # 读取post数据
    from_xml = request.body.read().decode()
    app.log.info("POST data: %s" % from_xml)
    # 接收消息解密
    ret, decrypt_xml = decrypt(from_xml, msg_signature, timestamp, nonce)
    app.log.info("Decrypt data: %s, %s" % (ret, decrypt_xml))

    s_xml = template('send_msg', touser=openid, fromuser=wx_account,
                     createtime=int(time.time()), content="thank you", msgid=extract(decrypt_xml, "MsgId"))
    app.log.info("Response xml: %s" % s_xml)
    # 加密返回消息字符串
    ret, to_xml = encrypt(s_xml, get_random_str(8))
    app.log.info("Response encrypt xml: %s" % to_xml)
    return to_xml


if __name__ == '__main__':
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
