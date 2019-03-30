# -*- coding: utf-8 -*-

import signal
from liship.setting import config


def quit():
    print('程序终止，正在保存任务......')

    with open(config['PRO_DIR'] + 'data/data.json') as fr:
        pass