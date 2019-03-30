# -*- coding: utf-8 -*-

import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def get_desired_capabilities(app=None, platform=None, device_name=None, appPackage=None, appActivity=None):
    desired_caps = {
        "platformName": "Android",
        "automationName": "Appium",
        "deviceName": device_name,
        "platformVersion": platform,
        "appPackage": appPackage,
        "appActivity": appActivity,
        "noReset": True,
        "unicodeKeyboard": True,
        "resetKeyboard": True
    }

    if app:
        desired_caps["app"] = app

    return desired_caps















