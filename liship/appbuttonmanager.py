# -*- coding: utf-8 -*-

from appium.webdriver.common.mobileby import MobileBy as By


class Button(object):
    def __init__(self, left_top=None, right_bottom=None, id=None, name=None, text=None, locator=None):
        self.left_top = left_top
        self.right_bottom = right_bottom
        self.id = id
        self.name = name
        self.text = text
        self.locator = locator


class AppButtonManager(object):
    @classmethod
    def checkout(cls, app_version='1.7.6', device_type='huawei-7p'):
        if app_version == '1.7.6':
            if device_type == 'nox':
                return cls.model_nox_simulator()
        elif app_version == '1.9.0':
            if device_type == 'huawei=7p':
                return cls.model_huawei_720_1280()
            elif device_type == '':
                pass

    @classmethod
    def model_nox_simulator(cls):
        return {

        }
















