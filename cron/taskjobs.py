#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from fund.fund_helpers import get_fund_codes


def print_job():
    print('print_job! The time is: %s' % (datetime.now()))


def creat_fund_list_file():
    get_fund_codes("fund/fund_codes.conf")
