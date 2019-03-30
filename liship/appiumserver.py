# -*- coding: utf-8 -*-

import subprocess


class AppiumServer(object):
    def __init__(self):
        pass

    def start(self, servers):
        for p, bp, udid in servers:
            r = subprocess.run(["appium", "-p", str(p), "-bp", str(bp), "-U", udid])









