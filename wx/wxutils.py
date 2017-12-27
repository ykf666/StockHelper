#!/usr/bin/env python
# coding=utf-8
import random
import string

wx_token = "RZmUQDAuNjf3y6i2kL0IX8WBMOpPraEY"


def wxtoken():
    return wx_token


def gen_random_str(length):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
    print(ran_str)


if __name__ == "__main__":
    gen_random_str(32)
