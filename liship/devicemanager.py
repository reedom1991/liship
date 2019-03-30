# -*- coding: utf-8 -*-

import arrow
import logging
from threading import Lock
import os

from liship.lishipapp import LiShiPApp
from liship.constant import Stat
from liship.utils.exception import *
from selenium.common.exceptions import WebDriverException
from liship.utils import retry
from liship.setting import config


device_stat_lock = Lock()
logger = logging.getLogger('liship')


class DeviceManager():
    def __init__(self, devices=None):
        self.devices = list()
        if devices:
            for ip, port, sip, sport in devices:
                device = Device(ip, port, sip, sport)
                self.devices.append(device)

    def add_device(self, device):
        for d in self.devices:
            if d.ip == device.ip and d.port == device.port:
                raise MultipleDeviceException(msg='设备已经存在[%s:%d]' % (device.ip, device.sip))
            if d.ip == device.sip and d.sport == device.sport:
                raise MultipleDeviceException(msg='添加设备失败[%s:%d], appium节点已经被[%s:%d]使用[%s:%d]' % (device.ip, device.port, device.sip, device.sport))
        self.devices.append(device)

    def get_device_prepared(self, udid=None):
        device_stat_lock.acquire()
        for device in self.devices:
            if not udid:
                if device.stat == Stat.PREPARED:
                    device.modify_stat(Stat.RUNNING)
                    device_stat_lock.release()
                    return device

            else:
                if device.stat == Stat.PREPARED and device.udid == udid:
                    device.modify_stat(Stat.RUNNING)
                    device_stat_lock.release()
                    return device
        device_stat_lock.release()

    def get_devices_prepared(self):
        devices = list()
        device_stat_lock.acquire()
        for device in self.devices:
            if device.stat == Stat.PREPARED:
                device.modify_stat(Stat.RUNNING)
                devices.append(device)
        device_stat_lock.release()
        return devices

    def check_device_stat(self, udid):
        for device in self.devices:
            if device.udid == udid:
                return device.stat

    def get_devices_stat(self):
        stats = []
        for device in self.devices:
            stats.append({
                'ip': device.ip,
                'port': device.port,
                'sip': device.sip,
                'sport': device.sport,
                'udid': device.udid,
                'platform': device.platform,
                'device_name': device.device_name,
                'device_type': device.device_type,
                'app': type(device.app).__name__,
                'stat': device.stat,
                'task': device.task.obj2dict() if device.task else dict()
            })

        return stats


class Device(object):
    def __init__(self, ip=None, port=None, sip=None, sport=None, udid=None, platform=None, device_name=None, device_type=None):
        self.ip = ip
        self.port = int(port)
        self.sip = sip
        self.sport = sport
        self.udid = udid
        self.platform = platform
        self.device_name = device_name
        self.device_type = device_type
        self.app = None
        self.start_time = arrow.now('local').timestamp
        self.stat = Stat.PREPARED
        self.task = None

    def install_app(self, app_name, app):
        if self.stat == Stat.PREPARED:
            self.app == LiShiPApp(self.sip, self.sport, app)
        return self.app

    def open_app(self, app_name):
        if app_name == 'liship':
            self.app = LiShiPApp(self.sip, self.sport, platform=self.platform, device_name=self.device_name, device_type=self.device_type)
        return self.app

    def modify_stat(self, stat):
        self.stat = stat

    @retry(times=3, forver=True)
    def do(self, command, thread_name, times=None):
        fh = logging.FileHandler(os.path.join(config['PRO_DIR'], './logs/liship-{}'.format(self.udid)))
        fm = logging.Formatter(config['LOGGING_CONFIG']['formatters']['f']['format'])
        fh.setFormatter(fm)
        thread_logger = logging.getLogger('liship.{}'.format(self.udid))
        thread_logger.addHandler(fh)
        thread_logger.setLevel(logging.DEBUG)
        try:
            thread_logger.debug("[%s]正在执行 command: %s" % (thread_name, command))
            app = self.open_app(command['app_name'])
            self.task = command
            thread_logger.debug("[%s]:成功打开app，马上执行命令" % thread_name)
            self.app.init_app()
            result = app.do(command, times)

        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            thread_logger.debug("[%s]: DeviceError" % thread_name)
            raise DeviceError(msg=e.msg + "[cmd]: %s" % command)
        except (ConnectionRefusedError, ConnectionResetError, URLError) as e:
            thread_logger.debug("[%s]: AppiumServerTimeout" % thread_name)
            raise AppiumServerTimeout(
                msg="[===到appium server的连接超时，请检查网络或确保appium server已经启动===]" + "[cmd]: %s" % command)
        except LiShiPFindTaskFailed as e:
            thread_logger.debug("[%s]:LiShiPFindTaskFailed" % thread_name)
            raise e
        except LiShiPLetterTaskFailed as e:
            thread_logger.debug("[%s]:LiShiPLetterTaskFailed" % thread_name)
        except InvalidSessionIdException as e:
            thread_logger.debug("[%s]: InvalidSessionIdException" % thread_name)
            e.msg = e.msg + "[cmd]: %s" % command
            raise e
        except Exception as e:
            thread_logger.debug("[%s]: 未预见的异常，需要处理" % thread_name)
            raise LiShiPUnknownException(msg="[%s]: 未预见的异常，需要处理，%s" % (thread_name, e))
        else:
            thread_logger.debug("[%s]: 执行完成" % thread_name)
        finally:
            if self.app:
                self.app.quit()
        self.modify_stat(Stat.PREPARED)
        thread_logger.debug("[%s]: 线程结束" % thread_name)

    def __str__(self):
        return "设备: [%s:%s] \n 开始运行时间: [%s] \n 已经运行了[%d]分钟" \
                %(self.ip, self.port,arrow.get(self.start_time), arrow.get(self.start_time).to('+8:00').isoformat())

    def __repr__(self):
        return self.__str__()




















