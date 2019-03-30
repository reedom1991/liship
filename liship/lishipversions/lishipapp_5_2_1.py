# -*- coding: utf-8 -*-

import time
from liship.app import App
from liship.constant import Task
from liship.desired_capabilities import get_desired_capabilities
from selenium.common.exceptions import (TimeoutException,
                                        NoSuchElementException,
                                        WebDriverException)
from liship.utils.exception import (LiShiPFindTaskFailed, LiShiPLetterTaskFailed)
from liship.appbuttonmanager import AppButtonManager


class Button(object):
    def __init__(self, left_top=None, right_bottom=None, id=None, name=None, text=None, locator=None):
        self.left_top = left_top
        self.right_bottom = right_bottom
        self.id = id
        self.name = name
        self.text = text
        self.locator = locator


class LiShiPApp_5_2_1(App):
    kol_letter_curren_sid_failed_times = 0

    def __init__(self, sip, sport, app=None, platform=None, device_name=None, device_type=None):
        desired_caps = get_desired_capabilities(app, platform=platform, device_name=device_name, appPackage='com.mobile.videonews.li.video', appActivity='com.mobile.videonews.li.video.act.main.MainTabAty')
        super(LiShiPApp_5_2_1, self).__init__(desired_caps, sip, sport)
        self.swip_to_next_wait_time = 5
        self.click_wait_time = 5
        self.swip_to_bottom_wait_time = 3
        self.find_wait_time = 3
        self.editor_wait_time = 0.5
        self.buttons = AppButtonManager.checkout(app_version='5.2.1', device_type=device_type)

    def init_app(self):
        self.sleep(13)
       # self.close_update_widget()
        self.move_to_next()

    def capture_info_page(self, attrs=None, command=None):
        if not attrs:
            attrs = ("comment", 'author', "following", "follower", "work", "like", 'music', 'music_hot', 'music_latest')

        if 'author' in attrs:
            if "following" in attrs:
                self.click_author_following()
                self.swip_to_bottom(10, 2, 1)
                self.click_back()
            if "follower" in attrs:
                self.click_author_follower()
                self.swip_to_bottom(10, 2, 1)
                self.click_back()
            if "follower" in attrs:
                self.click_author_follower()
                self.swip_to_bottom(10, 2, 1)
                self.click_back()
            if "work" in attrs:
                self.click_author_works()
                self.swip_to_bottom(50, 5)
            if "like" in attrs:
                self.click_author_like()
                self.swip_to_bottom(None, 5)
        if 'music' in attrs:
            self.click_music_info_xy()
            if 'music_hot' in attrs:
                self.click_music_hot()
                self.swip_to_bottom(None, 5)
            if 'music_latest' in attrs:
                self.click_music_latest()
                self.swip_to_bottom(None, 5)
            self.click_back()
        if "comment" in attrs:
            self.click_comment_xy()
            self.swip_to_bottom(10, 2, 1)
            self.click_back()

    def capture_music_info_page(self):
        self.click_music_info_xy()
        self.click_music_hot()
        self.swip_to_bottom(2, 5, 1)
        self.click_music_latest()
        self.swip_to_bottom(2, 5, 1)
        self.click_back()

    def move_to_next(self):
        self.swip(x1=int(0.5*self.window["width"]), y1=int(self.window['height']*0.9),
                  x2=int(0.5*self.window["width"]), y2=int(self.window['height']*0.1))
        self.sleep(self.swip_to_next_wait_time)

    def swip_to_bottom(self, max_assert=None, times_once_assert=None, wait=None):
        times_assert = 0
        while True:
            source_before = self.page_source
            for times in range(self.swip_times_every_assert if not times_once_assert else times_once_assert):
                self.swip(x1=int(0.2*self.window["width"]), y1=int(self.window['height']*0.8),
                          x2=int(0.2*self.window["width"]), y2=int(self.window['height']*0.1))
                source_after = self.page_source
                if source_before == source_after:
                    break
                times_assert += 1
                if max_assert and max_assert < times_assert:
                    break

    def set_up(self):
        super(LiShiPApp_5_2_1, self).set_up()
        self.sleep(3)
        while True:
            self.move_to_next()
            self.capture_author_info_page()
            self.capture_music_info_page()

    def click_author_follower(self):
        self.wait_element_clickable(self.buttons['author_follower_button'].locator).click()
        self.sleep(self.click_wait_time)

    def click_author_following(self):
        self.wait_element_clickable(self.buttons['author_following_button'].locator).click()
        self.sleep(self.click_wait_time)

    def click_find(self):
        self.wait_element_clickable(self.buttons['find_button'].locator).click()
        self.sleep(self.click_wait_time)

    def click_author_info_xy(self):
        click_by_xy(self.buttons['author_info_button'].left_top, self.buttons['author_info_button'].right_bottom)
        self.sleep(2)

    def click_back(self):
        self.driver.back()
        self.sleep(self.click_wait_time)

    def click(self):
        self.click_by_xy((0,0), tuple(self.window.values()))

    def close_update_widget(self):
        self.sleep(15)
        self.click_by_xy(self.buttons['not_update_buttom'].left_top, self.buttons['not_update_buttom'].right_bottom)
        self.click_back()

    def sleep(self, seconds):
        time.sleep(seconds)

    def do_finding(self, command, times=None):
        try:
            self.capture_author_info_by_shortid(command['data']['short_id'], attrs=command['data']['attrs'], command=command)
        except(TimeoutException, NoSuchElementException, WebDriverException) as e:
            if times >= 5:
                raise LiShiPFindTaskFailed(msg="抖音搜索任务失败")
            raise e

    def do_crawling(self, command):
        try:
            while True:
                self.capture_info_page(attrs=command['data']['attrs'], command=command)
                self.move_to_next()
        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            raise e

    #def do_kol_letter(self, command, times=None):

    def do_category(self, command, times=None):
        self.click_find_xy()
        self.swip_to_bottom(100, 10)

    def do(self, command, times):
        if command["task_type"] == Task.FINDING:
            self.do_finding(command, times)
        if command["task_type"] == Task.CRAWLING:
            self.do_crawling(command)
        if command["task_type"] == Task.KOL_LETTER:
            self.do_kol_letter(command, times)
        if command["task_type"] == Task.CATEGORY:
            self.do_category(command, times)















