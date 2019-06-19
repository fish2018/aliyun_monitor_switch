# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from retry import retry

# 阿里云监控大盘urls
URLS = ["URL1","URL2","URL3"]
# 用户名
USERNAME = "USERNAME"
# 密码
PASSWORD = "PASSWORD"
# 切换间隔时间
SWITCHTIME = 120


class Monitor(object):
    def __init__(self):
        self.urls = URLS
        self.switchtime = SWITCHTIME
        # 加启动配置,隐藏"Chrome正在受到自动软件的控制"
	option = webdriver.ChromeOptions()
	option.add_argument('disable-infobars')
        self.browser = webdriver.Chrome(chrome_options=option)
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
    @retry(tries=10, delay=1)
    def closebox(self):
        try:
            self.browser.find_element_by_css_selector("div.help-guide-step-header > i.topbar-sidebar-no").click()
        except Exception:
            pass

    # 切换全屏
    @retry(tries=10, delay=1)
    def fullscreen(self):
        try:
            self.browser.find_element_by_class_name("cms4service-hidden").click()
        except Exception:
            pass

    # 循环切换浏览器标签
    def loopswitch(self):
        handles = self.browser.window_handles  # 获取当前窗口句柄集合(列表类型)
        i = 0
        while True:
            for h in handles:
                self.browser.switch_to.window(h)
                if i is 0:
                    self.closebox()
                self.fullscreen()
                time.sleep(self.switchtime if self.switchtime >= 30 else 30)
            i += 1

    # 启动
    def start(self):
        self.login()
        self.openurls()
        self.loopswitch()


if __name__ == '__main__':
    Monitor().start()
