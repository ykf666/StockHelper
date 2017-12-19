#!/usr/bin/env python
# coding=utf-8

from bottle import default_app, get, run
from beaker.middleware import SessionMiddleware
import easyquotation

# 设置session参数
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 1200,
    'session.data_dir': '/tmp/stockHelper/sessions',
    'session.auto': True
}


@get('/index')
def callback():
    quotation = easyquotation.use('sina')
    return quotation.real('600728')
    # return 'Hello World!'


# 函数主入口
if __name__ == '__main__':
    app_argv = SessionMiddleware(default_app(), session_opts)
    run(app=app_argv, host='0.0.0.0', port=9090, debug=True, reloader=True)