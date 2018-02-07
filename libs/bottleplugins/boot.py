#!/usr/bin/env python
# coding=utf-8

import json
from apscheduler.schedulers.background import BackgroundScheduler
from cron import taskjobs
import inspect
import bottle


class Boot:
    name = 'boot'
    api = 2

    def __init__(self):
        pass

    def setup(self, app):
        config = app.config

        # 定时任务配置
        jobs_file = config.get('config_path.jobs_file', './config/jobs.json')
        app.log.info("cron.jobs_file = " + jobs_file)

        with open(jobs_file, 'r') as f:
            conf = json.load(f)
        if "jobs" in conf:
            sched_jobs = conf["jobs"]
        sched = BackgroundScheduler()
        for job in sched_jobs:
            if job.pop("enable").lower() == "true":
                app.log.info("add job " + job["func"])
                job["func"] = getattr(taskjobs, job["func"])
                sched.add_job(**job)
        # 启动定时任务
        add_jobs = sched.get_jobs()
        if add_jobs.__len__() > 0:
            sched.start()

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            # req = bottle.request
            # sig = inspect.getfullargspec(callback)
            #
            # for a in sig.args:
            #     if a in req.params:
            #         kwargs[a] = req.params[a]
            #
            result = callback(*args, **kwargs)
            return result
        return wrapper

    def close(self):
        pass
