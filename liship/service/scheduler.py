# -*- coding: utf-8 -*-

import sys
import os
import time
import subprocess
from liship.schedule import scheduler
from liship.devicemanager import Device
from liship.utils.exception import *


class SchedulerService(object):

    @classmethod
    def get_devices_stat(cls):
        stat = {}
        stat['stat'] = scheduler.device_manager.get_devices_stat()
        stat['waiting_tasks'] = scheduler._queue.qsize()
        if sys.platform == 'win32':
            r = os.system('tasklist | findstr node.exe > %s\\appium_process' % os.environ['TEMP'])
            if r == 0:
                with open(os.environ['TEMP']+'\\appium_process') as fr:
                    nodes = fr.readlines()
                stat['appium'] = nodes
        elif sys.platform.find('linux') >= 0:
            pass
        elif sys.platform == 'darwin':
            pass
        return stat

    @classmethod
    def restart_third_services(cls):
        cls.stop_third_services()
        cls.start_third_services()

    @classmethod
    def add_device(cls, cmd):
        try:
            scheduler.device_manager.add_device(Device(**(cmd['data'])))
        except MultipleDeviceException as e:
            return e.msg
        return 'success'

    @classmethod
    def start_third_services(cls, method=None):
        devices = scheduler.device_manager.devices
        if sys.platform == 'win32':
            if not method or method == 'usb':
                for device in devices:
                    subprocess.Popen(['appium', '-p',str(device.sport), '-bp', str(device.sport+1000), '-U', device.udid, '-log', 'appium-%s.log' % device.udid, '--log-level', 'error'], shell=True)
                    time.sleep(2)
            elif method == 'wifi':
                for device in devices:
                    subprocess.Popen(['appium', '-p', str(device.sport), '-bp', str(device.sport+1000), '-U', "%s:%d" % (device.ip, device.port), '--log', 'appium-%s.log' % device.udid, '--log-level', 'error'], shell=True)
                    subprocess.Popen(['adb', 'connect', '%s:%d' % (device.ip, device.port)], shell=True)
                    time.sleep(2)
        elif sys.platform.find('linux') >= 0:
            pass
        elif sys.platform == 'darwin':
            pass

    @classmethod
    def stop_third_services(cls):
        devices = scheduler.device_manager.get_devices_stat()
        if sys.platform == 'win32':
            subprocess.Popen(['adb', 'kill-server'], stdout=subprocess.PIPE, shell=True)
            os.system('task kill /im node.exe /f > %s\\restart_process' % os.environ['TEMP'])
        elif sys.platform.find('linux') >= 0:
            pass
        elif sys.platform == 'darwin':
            pass















