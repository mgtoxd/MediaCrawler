# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

MediaCrawler 是一个多平台自媒体数据采集工具，支持小红书、抖音、快手、B站、微博、贴吧、知乎等平台的数据爬取。

**核心技术原理：** 使用 Playwright 浏览器自动化框架登录并保存登录态，通过 JS 表达式获取签名参数，无需复杂的 JS 逆向工程。

## 开发环境设置

### 环境依赖
- **Python**: >= 3.11
- **Node.js**: >= 16.0.0（抖音和知乎签名需要）
- **包管理**: 使用 `uv`（推荐）或原生 `venv`

### 常用命令

```bash
# 安装依赖
uv sync
playwright install

# 运行爬虫（示例：小红书关键词搜索）
uv run main.py --platform xhs --lt qrcode --type search

# 查看完整帮助
uv run main.py --help

# 初始化数据库
uv run main.py --init_db sqlite

# 启动 WebUI 服务
uv run uvicorn api.main:app --port 8080 --reload

# 运行测试
uv run pytest
```

### 测试
- `test/` 目录包含单元测试
- `tests/` 目录包含集成测试
- 使用 pytest 运行测试

## 代码架构

### 核心设计模式

**工厂模式**: `CrawlerFactory` 根据平台名称创建对应的爬虫实例
```python
# main.py:50-67
CRAWLERS = {
    "xhs": XiaoHongShuCrawler,
    "dy": DouYinCrawler,
    # ... 其他平台
}
```

**抽象基类**: `base/base_crawler.py` 定义了以下抽象类
- `AbstractCrawler` - 爬虫基类
- `AbstractLogin` - 登录逻辑基类
- `AbstractApiClient` - API 客户端基类
- `AbstractStore` - 数据存储基类

### 目录结构说明

```
media_platform/
├── xhs/           # 小红书爬虫
├── douyin/        # 抖音爬虫
├── kuaishou/      # 快手爬虫
├── bilibili/      # B站爬虫
├── weibo/         # 微博爬虫
├── tieba/         # 贴吧爬虫
└── zhihu/         # 知乎爬虫
```

每个平台目录包含：
- `core.py` - 爬虫主类，继承 `AbstractCrawler`
- `client.py` - API 客户端，处理 HTTP 请求
- `login.py` - 登录逻辑（二维码/手机号/Cookie）
- `help.py` - 辅助函数和数据提取
- `field.py` - 数据模型字段定义
- `*_sign.py` / `playwright_sign.py` - 签名生成（某些平台需要）

### 配置系统

- `config/base_config.py` - 全局配置（被覆盖到全局 `config` 模块）
- `config/*_config.py` - 各平台特定配置
- `cmd_arg/arg.py` - 命令行参数解析（使用 Typer）

**重要**: 命令行参数会覆盖 `config/base_config.py` 中的同名配置。

### 数据存储层

`store/` 目录实现了多种存储方式：
- CSV、JSON、Excel 文件存储
- MySQL、SQLite、PostgreSQL、MongoDB 数据库存储

### 代理 IP 池

`proxy/` 目录实现了 IP 代理池支持：
- `proxy_ip_pool.py` - 代理池管理
- `providers/` - 不同代理服务商的适配器

### WebUI / API

`api/` 目录包含 FastAPI 服务：
- `main.py` - FastAPI 应用入口
- `routers/` - API 路由
- `schemas/` - 数据模型
- `services/` - 业务逻辑
- `webui/` - WebUI 前端页面

### CDP 模式（反检测）

项目支持两种浏览器运行模式：
1. **Playwright 模式** - 使用 Playwright 启动浏览器
2. **CDP 模式** - 使用用户现有的 Chrome/Edge 浏览器（推荐，反检测能力更强）

配置项（`config/base_config.py`）：
- `ENABLE_CDP_MODE = True` - 启用 CDP 模式
- `CUSTOM_BROWSER_PATH` - 自定义浏览器路径
- `CDP_DEBUG_PORT` - CDP 调试端口

## 爬取类型

支持三种爬取模式（通过 `--type` 参数指定）：
- `search` - 关键词搜索
- `detail` - 指定帖子/视频 ID 详情
- `creator` - 指定创作者主页数据

## 登录方式

支持三种登录方式（通过 `--lt` 参数指定）：
- `qrcode` - 扫码登录（推荐）
- `phone` - 手机号登录
- `cookie` - Cookie 登录

## 添加新平台支持

1. 在 `media_platform/` 下创建新平台目录
2. 实现继承 `AbstractCrawler` 的爬虫类
3. 在 `main.py` 的 `CrawlerFactory.CRAWLERS` 中注册
4. 在 `cmd_arg/arg.py` 的 `PlatformEnum` 中添加枚举
5. 在 `config/` 下添加平台特定配置文件

## 注意事项

- 项目仅供学习研究使用，遵守目标平台使用条款
- 爬取数据时请控制频率，避免对平台造成负担
- 登录态会保存在 `chrome_user_data/` 目录
- 签名相关的 JS 文件在 `libs/` 目录
