# -*- coding: utf-8 -*-

import uuid
from collections import Iterable
from liship.constant import Task
from liship.utils.exception import CommandInvalidException


class Command(object):
    def __init__(self, **kwargs):
        self.cmd = kwargs
        self.cmd['uuid'] = uuid.uuid4().hex
        if "app_name" not in self.cmd.keys():
            self.cmd['app_name'] = None
        if "task_type" not in self.cmd.keys():
            self.cmd['task_type'] = None
        if "timeout" not in self.cmd.keys():
            self.cmd['timeout'] = None
        if "data" not in self.cmd.keys():
            self.cmd['data'] = None
        if "udid" not in self.cmd.keys():
            self.cmd['udid'] = None

    @property
    def app_name(self):
        return self.cmd["app_name"]

    def __getitem__(self, item):
        return self.cmd[item]

    def __setitem__(self, key, value):
        self.cmd[key] = value

    def __str__(self):
        return self.cmd.__str__()

    def __repr__(self):
        return self.__str__()

    def obj2dict(self):
        return self.cmd

    def dict2obj(self, d):
        self.cmd = d


class LiShiPCommand(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not kwargs.get('app_name'):
            self.cmd['app_name'] = 'liship'
        if self.cmd['task_type'] == Task.CRAWLING:
            if 'attrs' not in self.cmd['data'].keys():
                self.cmd['data']['attrs'] = None
            elif not isinstance(self.cmd['data']['attrs'], Iterable):
                raise CommandInvalidException('data.attrs必须是迭代类型')
        if self.cmd['task_type'] == Task.FINDING:
            if 'short_id' not in self.cmd['data'].keys():
                raise CommandInvalidException('梨视频搜索必须要指定short_id')
            if 'attrs' not in self.cmd['data'].keys():
                self.cmd['data']['attrs'] = None
            elif not isinstance(self.cmd['data']['attrs'], Iterable):
                raise CommandInvalidException('data.attrs必须是迭代类型')
        if self.cmd['task_type'] == Task.ADD_DEVICE:
            if 'ip' not in self.cmd['data'].keys() or 'port' not in self.cmd['data'].keys():
                raise CommandInvalidException('必须要指定添加设备的信息')

    def is_force(self):
        return self.cmd['force']


























