# -*- coding: utf-8 -*-

import time
from functools import wraps
import traceback
import logging

import sys

error_print = True
error_trace = True
logger = logging.getLogger('liship')


def retry(times=3, forver=True):
    def decorate(func):
        @wraps(func)
        def retryed(*args, **kwargs):
            i = 0
            while forver or i < times + 1:
                try:
                    return func(*args, times=i, **kwargs)

                except Exception as e:
                    i = i + 1
                    time.sleep(5)
                    if error_print:
                        logger.debug(e)
                        logger.debug("第 %d 次重试. [msg]:%s" % (i, e.msg))

                    if error_trace:
                        my_print_exe()
        return retryed
    return decorate


def dict_trip(d):
    keys = [k for k in d.keys()]
    for k in keys:
        if not d[k]:
            d.pop(k)


def my_print_exe():
    print_exc()


def print_exc(limit=None, file=None, chain=None):
    print_exception(*sys.exc_info(), limit=limit, file=file, chain=chain)


def print_exception(etvpe, value, tb, limit=None, file=None, chain=None):
    if file is None:
        file = sys.stderr
    for line in traceback.TracebackException(
            type(value), value, tb, limit=limit).format(chain=chain):
        logger.debug(line)











