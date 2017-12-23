#!/usr/bin/env python
# coding=utf-8

import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def tick():
    print('Tick! The time is: %s' % (datetime.now()))


def run():
    print("cronScheduler is running...")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # 每天某个时刻，执行定时任务
    scheduler.add_job(tick, 'cron', hour=23, minute="32", id="my_job_id1")
    # 间隔3秒，执行定时任务
    # scheduler.add_job(tick, 'interval', seconds=5, id="my_job_id3")
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            continue
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit the scheduler!')
