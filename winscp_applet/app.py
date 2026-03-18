import sys
import time
import os

# 从 common.py 导入 JumpServer 标准数据模型和工具函数
from common import BaseApplication, wait_pid

# 仅在 Windows 平台上导入 UI 自动化库
if sys.platform == 'win32':
    from pywinauto import Application
    from pywinauto.controls.uia_controls import (ButtonWrapper, EditWrapper, MenuItemWrapper)
    from pywinauto.keyboard import send_keys

# WinSCP 的默认安装路径（请根据实际环境调整）
_default_path = r"C:\Program Files (x86)\WinSCP\WinSCP.exe"

class AppletApplication(BaseApplication):
    """
    WinSCP Applet 核心应用逻辑
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 细节 14：优先使用外部传入的 path，否则使用默认路径
        self.path = kwargs.get('app_path', _default_path)
        
        # 获取连接的基础元数据
        self.host = self.asset.address
        self.port = self.asset.get_protocol_port(self.protocol)
        self.username = self.account.username
        self.password = self.account.secret

        self.pid = None
        self.app = None

    def run(self):
        """
        自动化执行流：启动 -> 定位窗口 -> 填表 -> 登录
        """
        # 1. 启动 WinSCP
        if not os.path.exists(self.path):
            print(f"Error: WinSCP executable not found at {self.path}")
            return

        print(f"Starting {self.path}...")
        app = Application(backend='uia').start(self.path)
        self.pid = app.process
        self.app = app

        # 2. 等待登录窗口出现
        # 细节 15：WinSCP 启动后的第一个窗口通常叫 "Login"
        try:
            # 找到主窗口并定位
            main_window = app.window(title_re=".*WinSCP.*", control_type="Window")
            # 或者直接 app.top_window()，但为了稳健建议带 title
            login_dlg = main_window.child_window(title="Login", control_type="Window")
            login_dlg.wait('ready', timeout=20)
            
            # --- 以下是填表逻辑 ---

            # 输入主机名 (Host Name)
            host_edit = login_dlg.child_window(title="Host Name", auto_id="Host Name", control_type="Edit")
            EditWrapper(host_edit.element_info).set_edit_text(self.host)

            # 输入端口 (Port Number)
            port_edit = login_dlg.child_window(title="Port number", auto_id="Port Number", control_type="Edit")
            EditWrapper(port_edit.element_info).set_edit_text(str(self.port))

            # 输入用户名 (User Name)
            user_edit = login_dlg.child_window(title="User name", auto_id="User Name", control_type="Edit")
            EditWrapper(user_edit.element_info).set_edit_text(self.username)

            # 输入密码 (Password)
            pass_edit = login_dlg.child_window(title="Password", auto_id="Password", control_type="Edit")
            EditWrapper(pass_edit.element_info).set_edit_text(self.password)

            # 最后点击 "Login" 按钮
            login_btn = login_dlg.child_window(title="Login", auto_id="Login", control_type="Button")
            ButtonWrapper(login_btn.element_info).click()

            print("Automation completed successfully. Logged in to WinSCP.")

        except Exception as e:
            print(f"Automation logic failed: {e}")
            # 如果失败了，让用户能看到打印出的控件信息以供调试
            if 'main_window' in locals():
                print("--- DEBUG: Current Window Identifiers ---")
                main_window.print_control_identifiers()

    def wait(self):
        # 细节 16：一定要在 run 结束且应用已经登录运行后，调用 wait 保持 Python 进程
        if self.pid:
            wait_pid(self.pid)

if __name__ == '__main__':
    # 这里的 main 初始化由 JumpServer 传入的字典参数触发
    pass
