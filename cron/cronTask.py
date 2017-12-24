#!/usr/bin/env python
# coding=utf-8

import time
from easyquotation import use


def print_time(enter_time):
    print("now is", time.time(), "enter_the_box_time is", enter_time)


# print(time.time())
#
# Timer(5, print_time, (time.time(),)).start()
# Timer(5, print_time, (time.time(),)).start()
# print(time.time())

if __name__ == '__main__':
    quotation = use("tencent")
    print(quotation.real(600728))
