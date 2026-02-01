# AGENTS.md - MediaCrawler 项目指南

> 本文档面向 AI 编程助手，提供项目架构、开发规范和操作指南的快速参考。
# 一定要用中文对话，生成的一切注释，文档，除了代码之外能用中文都用中文

## 项目概述

**MediaCrawler** 是一个功能强大的多平台自媒体数据采集工具，支持小红书(xhs)、抖音(dy)、快手(ks)、B站(bili)、微博(wb)、贴吧(tieba)、知乎(zhihu)等主流平台的公开信息抓取。

**核心技术原理**：基于 [Playwright](https://playwright.dev/) 浏览器自动化框架登录并保存登录态，通过 JS 表达式获取签名参数，无需复杂的 JS 逆向工程。

**许可证**：NON-COMMERCIAL LEARNING LICENSE 1.1（非商业学习使用许可证）

---

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python >= 3.11 |
| 包管理 | uv (推荐) / pip |
| 浏览器自动化 | Playwright |
| Web 框架 | FastAPI (WebUI API) |
| TUI 框架 | Textual (终端界面) |
| 数据库 | MySQL, SQLite, PostgreSQL, MongoDB |
| 缓存 | Redis |
| 类型检查 | MyPy |
| 测试 | pytest |

---

## 项目结构

```
MediaCrawler/
├── main.py                     # 程序入口，包含 CrawlerFactory 工厂
├── var.py                      # 全局上下文变量（contextvars）
├── config/                     # 配置模块
│   ├── base_config.py          # 全局基础配置
│   ├── *_config.py             # 各平台特定配置
│   └── db_config.py            # 数据库配置
├── base/                       # 抽象基类定义
│   └── base_crawler.py         # AbstractCrawler, AbstractLogin, AbstractApiClient, AbstractStore
├── media_platform/             # 各平台爬虫实现
│   ├── xhs/                    # 小红书 (core.py, client.py, login.py, help.py, field.py)
│   ├── douyin/                 # 抖音
│   ├── kuaishou/               # 快手
│   ├── bilibili/               # B站
│   ├── weibo/                  # 微博
│   ├── tieba/                  # 贴吧
│   └── zhihu/                  # 知乎
├── store/                      # 数据存储层
│   ├── xhs/, douyin/, ...      # 各平台存储实现
│   └── excel_store_base.py     # Excel 存储基类
├── database/                   # 数据库连接与模型
│   ├── db.py                   # 数据库初始化
│   ├── db_session.py           # 会话管理
│   └── models.py               # ORM 模型
├── model/                      # 数据模型（Pydantic）
│   └── m_*.py                  # 各平台数据模型
├── proxy/                      # IP 代理池
│   ├── proxy_ip_pool.py        # 代理池管理
│   └── providers/              # 代理服务商适配器
├── tools/                      # 工具模块
│   ├── app_runner.py           # 异步应用生命周期管理
│   ├── cdp_browser.py          # CDP 浏览器管理
│   ├── browser_launcher.py     # 浏览器启动器
│   ├── async_file_writer.py    # 异步文件写入
│   └── utils.py                # 通用工具函数
├── api/                        # WebUI API (FastAPI)
│   ├── main.py                 # API 入口
│   ├── routers/                # 路由
│   ├── schemas/                # 数据模型
│   └── services/               # 业务逻辑
├── TUI/                        # 终端用户界面 (Textual)
│   ├── main.py                 # TUI 入口
│   └── app.py                  # 主应用逻辑
├── cmd_arg/                    # 命令行参数解析
│   └── arg.py                  # Typer 参数定义
├── test/                       # 单元测试
├── tests/                      # 集成测试
├── docs/                       # 文档
└── libs/                       # JS 签名相关库文件
```

---

## 开发环境设置

### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 安装浏览器驱动
uv run playwright install
```

### 2. 环境变量配置

复制 `.env.example` 为 `.env`，配置以下环境变量：

```bash
# 数据库配置（根据需要选择）
MYSQL_DB_HOST=localhost
MYSQL_DB_USER=root
MYSQL_DB_PWD=password
REDIS_DB_HOST=127.0.0.1
MONGODB_HOST=localhost
POSTGRES_DB_HOST=localhost

# 代理配置（可选）
KDL_USER_NAME=
KDL_USER_PWD=
WANDOU_APP_KEY=
```

---

## 常用命令

### 运行爬虫

```bash
# 小红书关键词搜索（扫码登录）
uv run main.py --platform xhs --lt qrcode --type search

# 抖音指定帖子详情
uv run main.py --platform dy --lt qrcode --type detail

# 快手创作者主页数据
uv run main.py --platform ks --lt qrcode --type creator

# 查看完整帮助
uv run main.py --help
```

### 数据库初始化

```bash
# 初始化 SQLite
uv run main.py --init_db sqlite

# 初始化 MySQL
uv run main.py --init_db mysql

# 初始化 PostgreSQL
uv run main.py --init_db postgres
```

### 启动服务

```bash
# 启动 WebUI 服务（默认端口 8080）
uv run uvicorn api.main:app --port 8080 --reload

# 启动 TUI 终端界面
uv run python -m TUI.main
```

### 测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest test/test_utils.py
```

---

## 核心架构设计

### 1. 工厂模式

`CrawlerFactory` 根据平台名称创建对应的爬虫实例：

```python
# main.py
CRAWLERS = {
    "xhs": XiaoHongShuCrawler,
    "dy": DouYinCrawler,
    "ks": KuaishouCrawler,
    "bili": BilibiliCrawler,
    "wb": WeiboCrawler,
    "tieba": TieBaCrawler,
    "zhihu": ZhihuCrawler,
}
```

### 2. 抽象基类

`base/base_crawler.py` 定义以下抽象类：

- `AbstractCrawler` - 爬虫基类，实现 `start()`, `search()`, `launch_browser()`
- `AbstractLogin` - 登录逻辑基类，支持二维码/手机号/Cookie 登录
- `AbstractApiClient` - API 客户端基类
- `AbstractStore` - 数据存储基类

### 3. 平台目录结构

每个平台目录包含标准文件：

```
media_platform/{platform}/
├── core.py           # 爬虫主类，继承 AbstractCrawler
├── client.py         # API 客户端，处理 HTTP 请求
├── login.py          # 登录逻辑
├── help.py           # 辅助函数和数据提取
├── field.py          # 数据模型字段定义
├── exception.py      # 自定义异常
└── *_sign.py         # 签名生成（部分平台）
```

### 4. 配置系统

- `config/base_config.py` - 全局配置（被导入到 `config` 模块命名空间）
- 命令行参数（`cmd_arg/arg.py`）会覆盖 `base_config.py` 中的同名配置

**关键配置项**：

```python
PLATFORM = "xhs"              # 平台选择
CRAWLER_TYPE = "search"       # 爬取类型: search | detail | creator
LOGIN_TYPE = "qrcode"         # 登录方式: qrcode | phone | cookie
SAVE_DATA_OPTION = "json"     # 存储格式: csv | json | sqlite | db | excel | postgres | mongodb
ENABLE_CDP_MODE = False       # 是否启用 CDP 模式（反检测）
```

### 5. 全局上下文变量

`var.py` 使用 `contextvars` 实现全局变量管理：

- `request_keyword_var` - 当前请求关键词
- `crawler_type_var` - 爬虫类型
- `comment_tasks_var` - 评论任务队列
- `db_conn_pool_var` - 数据库连接池

---

## 代码风格规范

### 1. 文件头版权说明

所有 Python 文件必须包含以下文件头：

```python
# -*- coding: utf-8 -*-
# Copyright (c) 2025 relakkes@gmail.com
#
# This file is part of MediaCrawler project.
# Repository: https://github.com/NanmiCoder/MediaCrawler
# GitHub: https://github.com/NanmiCoder
# Licensed under NON-COMMERCIAL LEARNING LICENSE 1.1
#

# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。
```

> **注意**：项目配置了 pre-commit hooks 自动检查和添加文件头，运行 `pre-commit install` 安装钩子。

### 2. 类型注解

- 使用 Python 3.11+ 类型注解语法
- 复杂类型使用 `typing` 模块：
  - `dict[str, Type[AbstractCrawler]]` 而非 `Dict[str, Type[AbstractCrawler]]`
  - `list[str]` 而非 `List[str]`
  - `str | None` 而非 `Optional[str]`

### 3. 异步代码规范

- 所有 IO 操作使用 `async/await`
- 爬虫主类方法（`start`, `search`）必须是异步的
- 使用 `async_playwright()` 上下文管理器

### 4. 日志记录

使用 `tools.utils.logger`：

```python
from tools import utils

utils.logger.info("[ModuleName] Message")
utils.logger.error("[ModuleName] Error: %s", error)
```

---

## 测试策略

### 测试目录结构

```
test/           # 单元测试
tests/          # 集成测试
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest test/test_utils.py -v

# 带覆盖率报告
uv run pytest --cov=. --cov-report=html
```

### 编写测试

- 测试文件命名：`test_*.py`
- 测试函数命名：`test_*`
- 异步测试使用 `pytest-asyncio`：

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data()
    assert result is not None
```

---

## 添加新平台支持

按照以下步骤添加新平台爬虫：

1. **创建平台目录**：`media_platform/new_platform/`

2. **实现核心类**：
   - `core.py` - 继承 `AbstractCrawler` 的爬虫类
   - `client.py` - 继承 `AbstractApiClient` 的 API 客户端
   - `login.py` - 继承 `AbstractLogin` 的登录类
   - `help.py` - 辅助函数
   - `field.py` - 字段定义
   - `exception.py` - 自定义异常

3. **注册爬虫**：在 `main.py` 的 `CrawlerFactory.CRAWLERS` 中添加映射

4. **添加配置**：在 `config/` 下创建 `{platform}_config.py`

5. **添加存储实现**：在 `store/{platform}/` 下创建存储类

6. **更新命令行参数**：在 `cmd_arg/arg.py` 的 `PlatformEnum` 中添加枚举值

---

## 数据存储

支持多种存储方式，通过 `SAVE_DATA_OPTION` 配置：

| 选项 | 说明 | 特点 |
|------|------|------|
| `json` | JSON 文件 | 默认，支持词云生成 |
| `csv` | CSV 文件 | 表格格式 |
| `excel` | Excel 文件 | 支持多工作表 |
| `sqlite` | SQLite 数据库 | 轻量级本地数据库 |
| `db` | MySQL 数据库 | 支持去重，生产推荐 |
| `postgres` | PostgreSQL 数据库 | 高级数据库功能 |
| `mongodb` | MongoDB | 文档型数据库 |

---

## CDP 模式（反检测）

项目支持两种浏览器运行模式：

1. **Playwright 模式** - 使用 Playwright 启动浏览器（默认）
2. **CDP 模式** - 使用用户现有的 Chrome/Edge 浏览器（推荐，反检测能力更强）

**启用 CDP 模式**：

```python
# config/base_config.py
ENABLE_CDP_MODE = True
CUSTOM_BROWSER_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CDP_DEBUG_PORT = 9222
```

---

## 安全与合规

### ⚠️ 重要提醒

1. **许可证限制**：本项目使用 NON-COMMERCIAL LEARNING LICENSE 1.1，**仅限学习和研究目的，禁止商业用途**

2. **法律合规**：
   - 遵守目标平台的使用条款和 robots.txt 规则
   - 不得进行大规模爬取或对平台造成运营干扰
   - 合理控制请求频率（通过 `CRAWLER_MAX_SLEEP_SEC` 配置）

3. **敏感信息**：
   - 用户登录态保存在 `chrome_user_data/` 目录
   - 不要将 `.env` 文件提交到版本控制
   - 代理配置等敏感信息通过环境变量管理

4. **请求频率控制**：
   - 配置 `CRAWLER_MAX_SLEEP_SEC` 控制爬取间隔
   - 配置 `MAX_CONCURRENCY_NUM` 控制并发数
   - 默认单并发，避免对平台造成负担

---

## 常见问题

### 1. 扫码登录失败

- 小红书：关闭 `HEADLESS = False`，手动过滑动验证码
- 抖音：检查是否出现手机号验证，手动验证后再试

### 2. 浏览器启动失败

- 确保已运行 `playwright install` 安装浏览器
- CDP 模式下确保 `CUSTOM_BROWSER_PATH` 指向正确的浏览器路径

### 3. 依赖冲突

使用 `uv sync` 而非 `pip install` 确保依赖版本一致性

---

## 参考资源

- **项目文档**: https://nanmicoder.github.io/MediaCrawler/
- **GitHub 仓库**: https://github.com/NanmiCoder/MediaCrawler
- **Playwright 文档**: https://playwright.dev/python/
- **FastAPI 文档**: https://fastapi.tiangolo.com/
- **Textual 文档**: https://textual.textualize.io/

---

## 联系方式

- **作者**: 程序员阿江-Relakkes
- **邮箱**: relakkes@gmail.com
- **微信**: relakkes
