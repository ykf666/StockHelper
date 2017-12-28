#!/usr/bin/env python
# coding=utf-8
import random
import string

wx_token = "RZmUQDAuNjf3y6i2kL0IX8WBMOpPraEY"
wx_encodingAESKey = "z4dGm7I9k5xtPDj7ucLgHK0xwCoIVGFOuOW90cOsnga"
wx_appid = "wx22b402d2c52b8ac1"


def wxtoken():
    return wx_token


def gen_random_str(length):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
    print(ran_str)


if __name__ == "__main__":
    gen_random_str(32)
