#!/usr/bin/env python
# coding=utf-8

import json
from apscheduler.schedulers.background import BackgroundScheduler
from bottle import Bottle, run, request
from cron import taskjobs
from urllib import parse
from canister import Canister

app = Bottle()
bottle_config = app.config.load_config("config/app.conf")
app.install(Canister())


@app.route('/')
def index():
    app.log.info("access web root index...")
    return "Welcome to python web!"


@app.route('/wx', method="POST")
def wx():
    # 读取url参数
    qs = parse.parse_qs(request.query_string)
    # 读取post数据
    fp = request.body.read().decode()
    app.log.info("POST data: %s" % fp)
    app.log.info("Signature: %s" % qs["signature"][0])
    return ""


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
