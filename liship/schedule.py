# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "\\...\\")
import pika
import json
import arrow
import threading
import queue
from liship.constant import Task, Stat
from liship.utils.exception import DeviceTimeoutException
from liship.utils import retry
from liship.devicemanager import DeviceManager, Device
from liship.command import LiShiPCommand


class Schedule(threading.Thread):
    def __init__(self, device_manager):
        super().__init__()
        self._queue = queue.Queue(maxsize=1000000)
        self.device_manager = device_manager

    def run(self):
        while True:
            if self._queue:
                cmd = self._queue.get(block=True)
                try:
                    self.excute(cmd)
                except DeviceTimeoutException as e:
                    print("DeviceTimeoutException")
                    import traceback
                    traceback.print_exc()

    @retry(forver=True)
    def excute(self, command, times=None):
        timeout = command['timeout']
        s = arrow.now().timestamp
        e = s + timeout if timeout else 0
        while not timeout or s <= e:
            device = self.device_manager.get_device_prepared(udid=command['udid'])
            if device:
                break
            else:
                s = arrow.now().timestamp
        else:
            raise DeviceTimeoutException(msg="没有可用的设备，正在等待设备就绪.....")
        t = threading.Thread(target=device.do, args=(command, device.udid))
        t.start()

    def push_command(self, command):
        self._queue.put(command)


def int2menu(t):
    if t == 1:
        return Task.FINDING
    if t == 2:
        return Task.CRAWLING
    if t == 4:
        return Task.ADD_DEVICE

dm = DeviceManager()
scheduler = Schedule(dm)


def main():
    print("1111111")
    devices = []
    device = ("127.0.0.1", 62025, "192.168.1.177", 4723)
    devices.append(device)
    dm = DeviceManager(devices)
    scheduler = Schedule(dm)
    scheduler.start()
    scheduler.push_command(LiShiPCommand(**{"task_type": Task.FINDING, "data": {"short_id": "kelly0711", "attrs":["following", "work", "like"]}}))

    def cb(ch, method, properties, body):
        data = json.loads(body.decode('utf-8'))
        data['task_type'] = int2menu(data['task_type'])
        print('收到命令', data)
        scheduler.push_command(LiShiPCommand(**data))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    con = pika.BlockingConnection(pika.ConnectionParameters(host='', port=5672, virtual_host='/',
                                                            credentials=pika.PlainCredentials('',
                                                                                              '')))
    channel = con.channel()
    channel.basic_consume(cb, queue="liship.task.cmd")
    channel.start_consuming()

if __name__ == '__main__':
    main()














