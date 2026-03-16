import time

from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from common import Asset, User, Account
from common import BaseApplication

class WebAPP(object):

    def __init__(
            self, app_name: str = '', user: User = None,
            asset: Asset = None, account: Account = None, **kwargs
    ):
        self.app_name = app_name
        self.user = user
        self.asset = asset
        self.account = account

class AppletApplication(BaseApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = None
        self.app = WebAPP(
            app_name=self.app_name, user=self.user, account=self.account, asset=self.asset
        )
        self._chrome_options = self.set_chrome_driver_options()

    @staticmethod
    def set_chrome_driver_options():
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # 禁用 扩展
        options.add_argument("--disable-extensions")
        # 忽略证书错误相关
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--allow-running-insecure-content')

        # 禁用开发者工具
        options.add_argument("--disable-dev-tools")
        # 禁用 密码管理器弹窗
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        return options

    def run(self):
        service = Service()
        #  driver 的 console 终端框不显示
        service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(options=self._chrome_options, service=service)
        self.driver.implicitly_wait(30)
        if self.account.username and self.account.secret:
            self.app.asset.address = self.app.asset.address.replace('://', f"://{self.account.username}:{self.account.secret}@")

        self.driver.get(self.app.asset.address)
        self.driver.maximize_window()

    def wait(self):
        disconnected_msg = "Unable to evaluate script: disconnected: not connected to DevTools\n"
        closed_msg = "Unable to evaluate script: no such window: target window already closed"

        while True:
            time.sleep(5)
            logs = self.driver.get_log('driver')
            if len(logs) == 0:
                continue
            ret = logs[-1]
            if isinstance(ret, dict):
                message = ret.get('message', '')
                if disconnected_msg in message or closed_msg in message:
                    break
                print("ret: ", ret)
        self.close()

    def close(self):
        if self.driver:
            try:
                # quit 退出全部打开的窗口
                self.driver.quit()
            except Exception as e:
                print(e)
