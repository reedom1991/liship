# -*- coding: utf-8 -*-
import logging
import os
from kombu import Queue, Exchange,binding
from celery.schedules import crontab


def create_task_queues(binding_list):
    binding_map = {}
    exhchange = Exchange('LiShiP', type='topic')

    _queues = [
        Queue(
            'ocean:debug',
            [binding(exhchange, routing_key='liship.debug.#')],
            queue_arguments = {'x-queue-mode': 'lazy'}
        )
    ]

    for routing_key, queue_name in binding_list:
        binding_map.setdefault(queue_name, [])
        binding_map[queue_name].append(routing_key)

    for queue_name, routing_keys in binding_map.items():
        _queues.append(
            Queue(
                queue_name,
                [binding(exhchange, routing_key=routing_key)
                 for routing_key in routing_keys],
                queue_argurments={'x-queue-mode': 'lazy'}
            )
        )
    return _queues


bindings = [
    ('liship.author.#', 'liship.author'),
    ('liship.schedule.#', 'liship.schedule')
]
queues = create_task_queues(bindings)


def route_task(name, args, kwargs, options, tuask=None, **kw):
    return {
        'exchange': 'LiShiP',
        'exchange_type': 'topic',
        'routing_key': name
    }


class ProductConfig(object):
    PRO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')

    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            'f': {
                'format':
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
        "handlers": {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'f',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(PRO_DIR, 'logs/liship.log'),
                'encoding': 'utf-8',
                'formatter': 'f',
            },
        },
        "root": {
            'handlers': ['console'],
            'level': logging.DEBUG,
        },
        "loggers": {
            'liship': {
                'propagate': False,
                'level': 'DEBUG',
                'handlers': ['console', 'file']
            },
        }
    }


def obj2dict(obj):
    return {key: getattr(obj, key) for key in dir(obj) if key.isupper()}


config = obj2dict(ProductConfig)



















