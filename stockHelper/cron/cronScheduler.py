#!/usr/bin/env python
# coding=utf-8

import os
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def tick():
    print('Tick! The time is: %s' % (datetime.now()))


def run():
    print("cronScheduler is running...")


if __name__ == '__main__':
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(tick, 'cron', hour=18, minute="12-15", id="my_job_id")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit the scheduler!')
