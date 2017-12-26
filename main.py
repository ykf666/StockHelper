#!/usr/bin/env python
# coding=utf-8

from bottle import default_app, get, run
from beaker.middleware import SessionMiddleware
# from cron import sched_task
from wxreporter import stock_report

# 设置session参数
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 1200,
    'session.data_dir': '/tmp/stockHelper/sessions',
    'session.auto': True
}


@get('/index')
def callback():
    return stock_report.summary_stock()


if __name__ == '__main__':
    # 启动定时任务
    # sched_task.run_task()
    app_argv = SessionMiddleware(default_app(), session_opts)
    run(app=app_argv, host='0.0.0.0', port=9090, debug=True, reloader=False)

