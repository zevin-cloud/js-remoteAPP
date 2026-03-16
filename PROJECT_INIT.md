# js-remoteAPP Project Init

## 项目定位

这个仓库不是常规业务系统代码仓库，而是一个用于开发 JumpServer Remote App / Applet 的工作区。

仓库当前包含三类内容：

1. 开发文档：说明 Applet 目录结构、参数来源、运行方式、连接模型。
2. 基础样例：`doc/basic_authentication/` 提供最小可运行模板。
3. 已完成实例：`ex/` 下提供可复用的完整压缩包样例。

## 当前目录结构

```text
.
├── doc/
│   ├── Applet+开发介绍.doc
│   ├── Applet+脚本的参数.doc
│   ├── Remote+App+连接示意图.doc
│   └── basic_authentication/
│       ├── app.py
│       ├── common.py
│       ├── main.py
│       ├── manifest.yml
│       ├── platform.yml
│       └── setup.yml
└── ex/
    ├── chrome.zip
    ├── dbeaver.zip
    └── navicat.zip
```

## 项目运行机制

JumpServer 的 Remote App 程序 `tinker` 会以类似下面的方式启动 applet：

```bash
python main.py <base64_json_data>
```

其中 `base64_json_data` 是连接授权信息的 base64 编码，解码后通常包含：

- `app_name`
- `protocol`
- `user`
- `asset`
- `account`
- `platform`

Applet 的职责通常是：

1. 解析 JumpServer 传入参数。
2. 根据资产和账号信息拉起浏览器或本地客户端。
3. 自动填充登录信息或拼接连接参数。
4. 在会话结束后等待并退出。

## 基础模板说明

`doc/basic_authentication/` 是最小模板，适合做新 applet 的起点。

- `main.py`：入口文件，读取 base64 参数并启动应用逻辑。
- `common.py`：通用数据模型和基础能力。
- `app.py`：具体连接逻辑，这个样例里是 Selenium 打开 Web 页面。
- `manifest.yml`：Applet 元数据。
- `platform.yml`：平台和协议定义。
- `setup.yml`：安装方式定义。

这个样例属于 Web 型 applet，核心方式是：

- 启动 Chrome WebDriver
- 将账号密码注入 URL 或页面表单
- 打开目标站点并保持会话

## 已完成实例的意义

`ex/` 里的压缩包可以当作真实生产样例：

- `chrome.zip`：Web 自动化型 applet，适合参考网页登录、步骤脚本、验证码处理等模式。
- `dbeaver.zip`：数据库客户端型 applet，适合参考本地程序启动和配置注入。
- `navicat.zip`：桌面客户端型 applet，适合参考安装包分发、初始化配置和封装发布。

## 一个完整 Applet 的常见文件

根据文档，一个完整 applet 目录通常会包含：

```text
icon.png
main.py
manifest.yml
platform.yml
setup.yml
build.yml
patch.yml
uninstall.yml
```

不是所有文件都必须存在。

常见规则：

- `main.py`、`manifest.yml`、`setup.yml` 一般是基础项。
- `platform.yml` 在需要自定义平台/协议时提供。
- `build.yml` 用于定义外部安装包下载地址。
- `patch.yml` 用于安装后的初始化配置。
- `uninstall.yml` 用于卸载逻辑。

## manifest / setup / platform 的职责

### `manifest.yml`

定义 applet 的元数据，例如：

- 名称
- 展示名
- 版本
- 作者
- 类型
- 支持协议
- 标签

### `setup.yml`

定义安装方式，例如：

- `msi`
- `exe`
- `zip`
- `manual`

常见字段包括：

- `type`
- `source`
- `arguments`
- `destination`
- `program`
- `md5`

### `platform.yml`

定义 JumpServer 中要同步创建的平台信息，例如：

- 自定义平台名
- 协议名和端口
- 自定义字段

这些字段最终会影响资产录入和 applet 运行时可拿到的 `asset/platform/spec_info` 数据。

## 这个仓库适合的开发方式

后续在这个仓库里开发新 applet，建议按下面顺序：

1. 先判断目标应用属于哪一类：
   - Web 页面自动登录
   - 本地桌面客户端启动
   - 数据库工具连接封装
2. 选一个最接近的样例做母版：
   - Web 类优先参考 `basic_authentication` 或 `chrome.zip`
   - 客户端类优先参考 `dbeaver.zip` 或 `navicat.zip`
3. 明确目标应用需要的最小输入：
   - 地址
   - 协议
   - 端口
   - 用户名
   - 密码
   - 额外字段
4. 再补齐：
   - `manifest.yml`
   - `platform.yml`
   - `setup.yml`
   - `main.py`
   - `app.py`
5. 最后处理安装、初始化和卸载。

## 我对当前项目的结论

当前仓库已经具备继续开发新 JumpServer applet 的基础条件，不缺方向，缺的是把下一个目标应用按现有模式落地。

最推荐的后续动作：

1. 解压并拆读 `chrome.zip`、`dbeaver.zip`、`navicat.zip`，整理成可直接复用的模板目录。
2. 选定下一个要接入的应用，基于最接近的样例开始开发。
3. 补一个统一 README，把文档、样例、打包方式和调试方法归并到仓库根目录。

## 当前协作约定

我接下来会默认把这个仓库当成 JumpServer applet 开发仓库来处理。

如果你让我“开发某个 jump server 应用”，我会优先按下面路径推进：

- 先选母版样例
- 再建目标 applet 目录
- 然后补齐 manifest/setup/platform/main/app
- 最后做验证和打包准备

