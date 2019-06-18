# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from retry import retry

# 阿里云监控大盘urls
URLS = [
    "https://cloudmonitor.console.aliyun.com/?spm=5176.2020520001.aliyun_sidebar.32.69864bd3bjEkG5#/dashboardnew/boardId=a75d5068-70cf-4fcc-bd9e-03cef58e1b1e&boardName=&timeSpan=1",
    "https://cloudmonitor.console.aliyun.com/?spm=5176.2020520001.aliyun_sidebar.32.69864bd3bjEkG5#/dashboardnew/boardId=b5df3782-a642-43fb-a709-4d6a99d46bd7&boardName=&timeSpan=1",
    "https://cloudmonitor.console.aliyun.com/?spm=5176.2020520001.aliyun_sidebar.32.69864bd3bjEkG5#/dashboardnew/boardId=2e2ae28c-43fa-4884-b85d-7aad61a35ed4&boardName=&timeSpan=1",
    "https://cloudmonitor.console.aliyun.com/?spm=5176.2020520001.aliyun_sidebar.32.69864bd3bjEkG5#/dashboardnew/boardId=664ccf03-dbac-421d-8d11-1c8e2920211b&boardName=&timeSpan=1",
    "https://cloudmonitor.console.aliyun.com/?spm=5176.2020520001.aliyun_sidebar.32.69864bd3bjEkG5#/dashboardnew/boardId=77fa8b9f-ff06-44aa-94e0-5e129531a2e1&boardName=&timeSpan=1"]
# 用户名
USERNAME = "devops@1294648747629870.onaliyun.com"
# 密码
PASSWORD = "devops@hhotel.com"
# 切换间隔时间
SWITCHTIME = 5


class Monitor(object):
    def __init__(self):
        self.urls = URLS
        self.switchtime = SWITCHTIME
        self.browser = webdriver.Chrome()
        self.username = USERNAME
        self.password = PASSWORD

    # 子账号登录阿里云监控
    def login(self):
        self.browser.get("https://signin.aliyun.com/login.htm")
        # 通过css_selector找到账号，密码的输入框，并输入相应的账号/密码
        self.browser.find_element_by_id("user_principal_name").send_keys(self.username)
        self.browser.find_element_by_class_name("next-btn").click()
        time.sleep(1)
        self.browser.find_element_by_id("password_ims").send_keys(self.password)
        self.browser.find_element_by_class_name("submit-btn").click()

    # 打开监控大盘页面
    def openurls(self):
        for index, u in enumerate(self.urls):
            if index is 0:
                self.browser.get(u)
            else:
                url = "window.open('%s');" % u
                self.browser.execute_script(url)

    # 关闭浮动框
    def closebox(self):
        try:
            self.browser.find_element_by_css_selector("div.help-guide-step-header > i.topbar-sidebar-no").click()
        except Exception:
            pass

    # 切换全屏
    @retry(tries=7, delay=0.5)
    def fullscreen(self):
        try:
            self.browser.find_element_by_class_name("cms4service-hidden").click()
        except Exception:
            pass

    # 循环切换浏览器标签
    def loopswitch(self):
        handles = self.browser.window_handles  # 获取当前窗口句柄集合(列表类型)
        while True:
            for h in handles:
                self.browser.switch_to.window(h)
                self.closebox()
                self.fullscreen()
                time.sleep(self.switchtime)

    # 启动
    def start(self):
        self.login()
        self.openurls()
        self.loopswitch()


if __name__ == '__main__':
    Monitor().start()
