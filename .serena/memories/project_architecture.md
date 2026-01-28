# 项目架构概览

MediaCrawler 是一个多平台自媒体数据采集工具，使用工厂模式和抽象基类设计。

## 核心架构

### 入口点
- `main.py` - 使用 `CrawlerFactory` 创建平台特定的爬虫实例

### 抽象基类 (base/base_crawler.py)
- `AbstractCrawler` - 爬虫基类
- `AbstractLogin` - 登录逻辑基类
- `AbstractApiClient` - API 客户端基类
- `AbstractStore` - 数据存储基类

### 平台实现 (media_platform/)
每个平台包含：core.py (爬虫主类)、client.py (API客户端)、login.py (登录逻辑)、help.py (辅助函数)

支持平台：xhs (小红书)、dy (抖音)、ks (快手)、bili (B站)、wb (微博)、tieba (贴吧)、zhihu (知乎)

### 数据存储 (store/)
支持多种存储：CSV、JSON、Excel、MySQL、SQLite、PostgreSQL、MongoDB

### 配置系统
- `config/base_config.py` - 全局配置
- `cmd_arg/arg.py` - 命令行参数解析（使用 Typer）
- 命令行参数会覆盖配置文件

### 代理 IP (proxy/)
代理池管理，支持多个代理服务商

## 技术栈
- Playwright - 浏览器自动化
- CDP (Chrome DevTools Protocol) - 反检测模式
- asyncio - 异步编程
- Typer - CLI 参数解析
- FastAPI - WebUI/API 服务

## 爬取类型
- search - 关键词搜索
- detail - 指定帖子详情
- creator - 创作者主页数据

## 登录方式
- qrcode - 扫码登录
- phone - 手机号登录
- cookie - Cookie 登录
