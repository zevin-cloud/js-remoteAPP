import sys

import win32api
import win32con
import win32gui

if sys.platform == 'win32':
    from pywinauto import Application
    from pywinauto.controls.uia_controls import (ButtonWrapper, EditWrapper, MenuItemWrapper,
                                                 MenuWrapper, ComboBoxWrapper, ToolbarWrapper)
    from pywinauto.keyboard import send_keys
from common import (BaseApplication, wait_pid, )

_default_path = r"C:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe"


class AppletApplication(BaseApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = _default_path
        self.username = self.asset.info.username
        self.password = self.asset.info.password
        self.host = self.asset.address
        self.port = self.asset.info.port
        self.original_host = self.asset.address
        self.original_port = self.asset.info.port
        self.is_gateway_connection = False
        if self.tinker_forward:
            self.is_gateway_connection = True
            self.host = self.tinker_forward.host
            self.port = self.tinker_forward.port

        self.db = self.asset.info.db_name
        self.pid = None
        self.app = None

    def run(self):
        app = Application(backend='uia')
        app.start(self.path)
        self.pid = app.process
        if not all([self.username, self.password, self.host]):
            print(f'缺少必要的参数')
            return

        menubar = app.window(title="MySQL Workbench", auto_id="MainForm", control_type="Window") \
            .child_window(title="Database", control_type="MenuItem")
        menubar.wait('ready', timeout=10, retry_interval=5)
        MenuItemWrapper(menubar.element_info).select()
        cdb = menubar.child_window(title="Connect to Database", control_type="MenuItem")
        cdb.wait('ready', timeout=10, retry_interval=5)
        MenuItemWrapper(cdb.element_info).click_input()

        if self.is_gateway_connection:
            to_local_socket_pipe = "{TAB}{DOWN 1}"
            send_keys(to_local_socket_pipe)
            to_standard_tcp_ip_over_ssh = ""
            for i in range(10):
                to_standard_tcp_ip_over_ssh = to_standard_tcp_ip_over_ssh + "{TAB}"
            to_standard_tcp_ip_over_ssh = to_standard_tcp_ip_over_ssh + "{DOWN 1}"
            send_keys(to_standard_tcp_ip_over_ssh)

            # 输入 SSH Hostname
            ssh_hostname_text = str(self.gateway.address) + ":" + str(self.gateway.protocols[0].port)
            ssh_hostname_ele = app.top_window().child_window(title="SSH Host Name", auto_id="SSH Host Name", control_type="Edit")
            EditWrapper(ssh_hostname_ele.element_info).set_edit_text(ssh_hostname_text)

            # 输入 SSH Username
            ssh_username_text = self.gateway.account.username
            ssh_username_ele = app.top_window().child_window(title="SSH Username", auto_id="SSH Username", control_type="Edit")
            EditWrapper(ssh_username_ele.element_info).set_edit_text(ssh_username_text)

            send_keys("{TAB}{ENTER}")

            # 输入 gateway password
            gateway_password = self.gateway.account.secret
            gateway_password_ele = app.top_window().child_window(title="Password", auto_id="Password", control_type="Edit")
            gateway_password_ele.wait('ready', timeout=10, retry_interval=5)
            EditWrapper(gateway_password_ele.element_info).set_edit_text(gateway_password)

            ok_ele = app.top_window().child_window(title="Button Bar", auto_id="Button Bar", control_type="Pane") \
                .child_window(title="OK", control_type="Button")
            ButtonWrapper(ok_ele.element_info).click()

            # 输入 MySQL Hostname
            mysql_hostname_text = self.original_host
            mysql_hostname_ele = app.top_window().child_window(title="MySQL Host Name", auto_id="MySQL Host Name", control_type="Edit")
            EditWrapper(mysql_hostname_ele.element_info).set_edit_text(mysql_hostname_text)

            # 输入 MySQL Server Port
            mysql_server_port_text = self.asset.info.port
            mysql_server_port_ele = app.top_window().child_window(title="MySQL Server Port", auto_id="MySQL Server Port", control_type="Edit")
            EditWrapper(mysql_server_port_ele.element_info).set_edit_text(mysql_server_port_text)

            # 输入 Username
            username_text = self.asset.info.username
            username_ele = app.top_window().child_window(title="User Name", auto_id="User Name", control_type="Edit")
            EditWrapper(username_ele.element_info).set_edit_text(username_text)

            send_keys("{TAB}{ENTER}")

            # 输入 password
            password_text = self.account.secret
            password_ele = app.top_window().child_window(title="Password", auto_id="Password", control_type="Edit")
            password_ele.wait('ready', timeout=10, retry_interval=5)
            EditWrapper(password_ele.element_info).set_edit_text(password_text)

            ok_ele = app.top_window().child_window(title="Button Bar", auto_id="Button Bar", control_type="Pane") \
                .child_window(title="OK", control_type="Button")
            ButtonWrapper(ok_ele.element_info).click()

            # 输入 db
            db_text = self.asset.info.db_name
            db_ele = app.top_window().child_window(title="Default Schema", auto_id="Default Schema", control_type="Edit")
            EditWrapper(db_ele.element_info).set_edit_text(db_text)

            ok_ele = app.top_window().child_window(title="Connection", auto_id="Connection", control_type="Window") \
                .child_window(title="OK", control_type="Button")
            ButtonWrapper(ok_ele.element_info).click()
        else:
            # 输入 host
            host_ele = app.top_window().child_window(title="Host Name", auto_id="Host Name", control_type="Edit")
            EditWrapper(host_ele.element_info).set_edit_text(self.host)

            # 输入 port
            port_ele = app.top_window().child_window(title="Port", auto_id="Port", control_type="Edit")
            EditWrapper(port_ele.element_info).set_edit_text(self.port)

            # 输入 username
            user_ele = app.top_window().child_window(title="User Name", auto_id="User Name", control_type="Edit")
            EditWrapper(user_ele.element_info).set_edit_text(self.username)

            # 输入 db
            db_ele = app.top_window().child_window(title="Default Schema", auto_id="Default Schema", control_type="Edit")
            EditWrapper(db_ele.element_info).set_edit_text(self.db)

            ok_ele = app.top_window().child_window(title="Connection", auto_id="Connection", control_type="Window") \
                .child_window(title="OK", control_type="Button")
            ButtonWrapper(ok_ele.element_info).click()

            # 输入 password
            password_ele = app.top_window().child_window(title="Password", auto_id="Password", control_type="Edit")
            password_ele.wait('ready', timeout=10, retry_interval=5)
            EditWrapper(password_ele.element_info).set_edit_text(self.password)

            ok_ele = app.top_window().child_window(title="Button Bar", auto_id="Button Bar", control_type="Pane") \
                .child_window(title="OK", control_type="Button")
            ButtonWrapper(ok_ele.element_info).click()
        self.app = app

    def wait(self):
        wait_pid(self.pid)