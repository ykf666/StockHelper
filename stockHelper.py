#!/usr/bin/env python
# coding=utf-8

import json
from apscheduler.schedulers.background import BackgroundScheduler
from bottle import Bottle, run, request
from cron import taskjobs
from urllib import parse
from bottleplugins.canister import Canister
from wx.wxapi import decrypt

app = Bottle()
bottle_config = app.config.load_config("config/app.conf")
app.install(Canister())


@app.route('/')
def index():
    # app.log.info("access web root index...")
    return "Welcome to python web!"


@app.route('/wx', method="POST")
def wx():
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

    ret, decrypt_xml = decrypt(from_xml, msg_signature, timestamp, nonce)
    app.log.info("Decrypt result: %s, %s" % (ret, decrypt_xml))

    return openid


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
