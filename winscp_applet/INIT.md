# WinSCP Applet 任务书

已经从 `dbeaver` 成功移植了 **`main.py`** 和 **`common.py`**。
当前重点在于完成 **`app.py`** 中的 WinSCP UI 自动化。

---

## 1. 任务进度

- [x] 基础设施搭建 (main.py, common.py, manifest.yml)
- [ ] UI 自动化逻辑开发 (app.py)
- [ ] 补丁与环境配置 (platform.yml, setup.yml)

---

## 2. 接下来需要你执行的工作 (在 Windows 环境下)

1. **确定路径**：打开 `app.py`，确认 `_default_path` 是否为您本地 WinSCP 的安装目录。
2. **确认窗口标题**：
   - 手动运行 WinSCP。
   - 确认登录界面的第一级窗口标题是 “Login” 还是 “Login - WinSCP”？
3. **获取 UI 属性**：
   - 使用 `Inspect.exe` 或运行我们稍后编写的测试脚本获取：
     - 主机名输入框、用户名输入框、密码输入框的 `Name` 或 `AutomationId`。

---

## 3. 下一步行动

1. [ ] 编写基础的 `app.py` 启动逻辑并抓取窗口句柄。
2. [ ] 逐步实现 IP -> 用户名 -> 密码的输入。
3. [ ] 进行 `base64` token 测试。
