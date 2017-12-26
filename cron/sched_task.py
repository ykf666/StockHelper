#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


# 获取股市综合指数行情
def my_job_1():
    print('Tick! The time is: %s' % (datetime.now()))


# def run_task():
    s = BackgroundScheduler()
    # s.add_job(my_job_1, 'cron', hour=16, minute="54", id="job_1")
    s.add_job(my_job_1, 'interval', seconds=60, id="job_1")
    s.start()
    print("apscheduler task is running...")
