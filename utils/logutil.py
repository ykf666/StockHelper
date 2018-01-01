#!/usr/bin/env python
# coding=utf-8

import logging


def getlogger():
    logger = logging.getLogger('applogger')
    f = logging.Formatter('%(asctime)s %(levelname)-4s [%(threadName)s]   %(message)s')
    logger.setLevel('INFO')
    ch = logging.StreamHandler()

    ch.setFormatter(f)
    logger.addHandler(ch)

    return logger
