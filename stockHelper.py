#!/usr/bin/env python
# coding=utf-8

import json
from apscheduler.schedulers.background import BackgroundScheduler
from beaker.middleware import SessionMiddleware
from bottle import Bottle, run, request
from cron import taskjobs

app = Bottle()
bottle_config = {
    'host': 'localhost',
    'port': 8080,
    'debug': False
}

# 设置session参数
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 1200,
    'session.data_dir': '/tmp/stockHelper/sessions',
    'session.auto': True
}


@app.route('/')
def index():
    print(request.environ.get("beaker.session"))
    return "welcome to my world!"


@app.route('/wx')
def wx():
    p_dict = request.params.dict
    print(p_dict)
    return p_dict["echostr"]


if __name__ == '__main__':
    with open("config.json", 'r') as f:
        conf = json.load(f)
    if "session" in conf:
        session_opts = conf["session"]
    if "bottle" in conf:
        bottle_config = conf["bottle"]
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
    app_argv = SessionMiddleware(app, session_opts)
    run(app=app_argv, **bottle_config)
