# -*- coding: utf-8 -*-

from liship.api import liship
from liship.command import LiShiPCommand
from liship.constant import Task
from liship.schedule import scheduler
from flask import request
import json
from liship.service.scheduler import SchedulerService


@liship.route("/hello", methods=['GET'])
def hello():
    return 'hello'


@liship.route('/task/crawling/', methods=['POST'])
def task_crawling():
    cmd = LiShiPCommand(timeout=int(request.args.get('timeout', 0)), task_type=Task.CRAWLING, data=json.loads(request.data.decode('utf-8')))
    scheduler.push_command(cmd)
    return cmd.__str__()


@liship.route('/task/device/', methods=['POST'])
def task_device_add():
    cmd = LiShiPCommand(timeout=int(request.args.get('timeout', 0)), task_type=Task.ADD_DEVICE, data=json.loads(request.data.decode('utf-8')))
    return SchedulerService.add_device(cmd)
















