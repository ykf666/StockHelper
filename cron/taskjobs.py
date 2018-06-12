#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from libs.easyquotation.helpers import update_stock_info_sqlite3


def print_job():
    print('print_job! The time is: %s' % (datetime.now()))


def init_stock_infos_job():
    update_stock_info_sqlite3()



