# -*- coding: utf-8 -*-

from appium.common.exceptions import NoSuchContextException
from selenium.common.exceptions import *
from urllib.error import URLError


class LiShiPTimeoutException(TimeoutException):
    pass


class DeviceTimeoutException(TimeoutException):
    pass


class LiShiPElementTimeoutException(NoSuchElementException):
    pass


class AppNotFindException(Exception):
    pass


class LiShiPFindTaskFailed(Exception):
    def __init__(self, msg):
        self.msg = msg
    pass


class LiShiPLetterTaskFailed(Exception):
    def __init__(self, msg):
        self.msg = msg
    pass

class LiShiPUnknownException(Exception):
    def __init__(self, msg):
        self.msg = msg
    pass


class AppiumServerTimeout(URLError):
    def __init__(self, msg=None):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return '<urlopen error %s>' % self.msg


class DeviceError(WebDriverException):
    pass


class CommandInvalidException(Exception):
    pass


class MultipleDeviceException(Exception):
    def __init__(self, msg=None):
        super().__init__(msg)
        self.msg = msg

















