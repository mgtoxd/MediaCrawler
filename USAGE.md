# MediaCrawler 命令行使用完整指南

## 目录

- [基本用法](#基本用法)
- [支持的爬取平台](#支持的爬取平台)
- [命令行参数详解](#命令行参数详解)
- [使用场景示例](#使用场景示例)
- [配置文件说明](#配置文件说明)
- [注意事项](#注意事项)

---

## 基本用法

### 标准命令格式

```bash
uv run main.py [OPTIONS]
```

### 最简单的使用示例

```bash
# 小红书关键词搜索（扫码登录）
uv run main.py --platform xhs --lt qrcode --type search

# 查看完整帮助信息
uv run main.py --help
```

---

## 支持的爬取平台

| 平台代码 | 平台名称 | 说明 |
|---------|---------|------|
| `xhs` | 小红书 | 支持搜索、详情、创作者模式 |
| `dy` | 抖音 | 支持搜索、详情、创作者模式 |
| `ks` | 快手 | 支持搜索、详情、创作者模式 |
| `bili` | B站 | 支持搜索、详情、创作者模式 |
| `wb` | 微博 | 支持搜索、详情、创作者模式 |
| `tieba` | 贴吧 | 支持搜索、详情、创作者模式 |
| `zhihu` | 知乎 | 支持搜索、详情、创作者模式 |

---

## 命令行参数详解

### 基础配置

#### `--platform` <平台>
选择要爬取的媒体平台。

**可选值：** `xhs` | `dy` | `ks` | `bili` | `wb` | `tieba` | `zhihu`
**默认值：** `xhs`
**示例：**
```bash
--platform xhs      # 小红书
--platform dy       # 抖音
--platform bili     # B站
```

#### `--type` <爬取类型>
指定爬取模式类型。

**可选值：**
- `search` - 关键词搜索模式
- `detail` - 指定帖子/视频详情模式
- `creator` - 指定创作者主页模式

**默认值：** `search`
**示例：**
```bash
--type search      # 关键词搜索
--type detail      # 指定帖子详情
--type creator     # 创作者主页
```

#### `--keywords` <关键词>
关键词搜索配置，多个关键词用英文逗号分隔。

**默认值：** `编程副业,编程兼职`
**适用模式：** `search`
**示例：**
```bash
--keywords "人工智能,机器学习"
--keywords "美食"
```

#### `--start` <页码>
爬取开始页码。

**默认值：** `1`
**适用模式：** `search`
**示例：**
```bash
--start 1      # 从第1页开始
--start 5      # 从第5页开始
```

#### `--specified_id` <ID列表>
指定帖子/视频的ID列表，用于详情模式。多个ID用逗号分隔，支持完整URL或纯ID。

**适用模式：** `detail`
**示例：**
```bash
# 使用纯ID
--specified_id "64b95d01000000000c034587,64b95d01000000000c034588"

# 使用完整URL（小红书）
--specified_id "https://www.xiaohongshu.com/explore/64b95d01000000000c034587"

# B站视频
--specified_id "BV1xx411c7mD"

# 微博
--specified_id "4982041758140155"
```

#### `--creator_id` <创作者ID列表>
指定创作者的ID列表，用于创作者模式。多个ID用逗号分隔，支持完整URL或纯ID。

**适用模式：** `creator`
**示例：**
```bash
# 使用纯ID
--creator_id "6129d00a0000000001002b57,6129d00a0000000001002b58"

# 使用完整URL（小红书）
--creator_id "https://www.xiaohongshu.com/user/profile/6129d00a0000000001002b57"

# B站用户
--creator_id "123456789"

# 微博用户
--creator_id "7797463367"
```

---

### 账户配置

#### `--lt` <登录方式>
指定登录方式。

**可选值：**
- `qrcode` - 扫码登录（推荐）
- `phone` - 手机号登录
- `cookie` - Cookie登录

**默认值：** `qrcode`
**示例：**
```bash
--lt qrcode     # 扫码登录
--lt phone      # 手机号登录
--lt cookie     # Cookie登录
```

#### `--cookies` <Cookie值>
用于Cookie登录方式的Cookie值。

**适用模式：** 当 `--lt cookie` 时使用
**示例：**
```bash
--lt cookie --cookies "your_cookie_string_here"
```

---

### 评论配置

#### `--get_comment` <是否爬取一级评论>
是否爬取帖子/视频的一级评论。

**可选值：** `yes` | `true` | `t` | `y` | `1` | `no` | `false` | `f` | `n` | `0`
**默认值：** `False`
**示例：**
```bash
--get_comment yes      # 启用一级评论爬取
--get_comment true     # 启用一级评论爬取
--get_comment 1        # 启用一级评论爬取
--get_comment no       # 禁用一级评论爬取
```

#### `--get_sub_comment` <是否爬取二级评论>
是否爬取评论的二级回复。

**可选值：** `yes` | `true` | `t` | `y` | `1` | `no` | `false` | `f` | `n` | `0`
**默认值：** `False`
**示例：**
```bash
--get_sub_comment yes   # 启用二级评论爬取
--get_sub_comment no    # 禁用二级评论爬取
```

#### `--max_comments_count_singlenotes` <数量>
单个帖子/视频爬取的一级评论最大数量。

**默认值：** `10`
**示例：**
```bash
--max_comments_count_singlenotes 50    # 每个帖子最多爬50条评论
--max_comments_count_singlenotes 100   # 每个帖子最多爬100条评论
```

---

### 运行时配置

#### `--headless` <无头模式>
是否启用无头浏览器模式（不显示浏览器窗口）。适用于 Playwright 和 CDP 两种模式。

**可选值：** `yes` | `true` | `t` | `y` | `1` | `no` | `false` | `f` | `n` | `0`
**默认值：** `False`
**说明：**
- 设置为 `False` 会打开浏览器窗口，便于调试和手动处理验证码
- 小红书如果一直扫码登录不通过，建议设置为 `false` 打开浏览器手动过滑动验证码
- 抖音如果一直提示失败，打开浏览器看是否扫码后出现手机号验证

**示例：**
```bash
--headless no      # 显示浏览器窗口
--headless yes     # 不显示浏览器窗口
```

---

### 存储配置

#### `--save_data_option` <存储方式>
数据保存方式。

**可选值：**
- `csv` - 保存为CSV文件
- `json` - 保存为JSON文件（默认）
- `excel` - 保存为Excel文件
- `db` - 保存到MySQL数据库
- `sqlite` - 保存到SQLite数据库
- `mongodb` - 保存到MongoDB数据库
- `postgres` - 保存到PostgreSQL数据库

**默认值：** `json`
**示例：**
```bash
--save_data_option json        # JSON文件
--save_data_option csv         # CSV文件
--save_data_option excel       # Excel文件
--save_data_option sqlite      # SQLite数据库
--save_data_option db          # MySQL数据库
--save_data_option postgres    # PostgreSQL数据库
--save_data_option mongodb     # MongoDB数据库
```

#### `--init_db` <数据库类型>
初始化数据库表结构。

**可选值：** `sqlite` | `mysql` | `postgres`
**说明：** 执行此参数后会初始化对应数据库的表结构，然后程序退出
**示例：**
```bash
# 初始化SQLite数据库（最简单）
uv run main.py --init_db sqlite

# 初始化MySQL数据库
uv run main.py --init_db mysql

# 初始化PostgreSQL数据库
uv run main.py --init_db postgres
```

---

## 使用场景示例

### 场景1: 小红书关键词搜索

```bash
# 搜索"美食"相关的笔记
uv run main.py --platform xhs --lt qrcode --type search --keywords "美食"

# 搜索多个关键词并启用评论爬取
uv run main.py --platform xhs --lt qrcode --type search --keywords "人工智能,机器学习" --get_comment yes

# 从第5页开始搜索
uv run main.py --platform xhs --lt qrcode --type search --keywords "编程" --start 5
```

### 场景2: 获取指定帖子详情

```bash
# 获取指定小红书笔记详情
uv run main.py --platform xhs --lt qrcode --type detail --specified_id "64b95d01000000000c034587"

# 获取多个帖子详情并爬取评论
uv run main.py --platform xhs --lt qrcode --type detail --specified_id "id1,id2,id3" --get_comment yes --get_sub_comment yes

# B站视频详情
uv run main.py --platform bili --lt qrcode --type detail --specified_id "BV1xx411c7mD"

# 微博详情
uv run main.py --platform wb --lt qrcode --type detail --specified_id "4982041758140155"
```

### 场景3: 获取创作者主页数据

```bash
# 获取指定小红书创作者主页数据
uv run main.py --platform xhs --lt qrcode --type creator --creator_id "6129d00a0000000001002b57"

# 获取多个创作者数据
uv run main.py --platform xhs --lt qrcode --type creator --creator_id "creator1,creator2,creator3"

# B站UP主数据
uv run main.py --platform bili --lt qrcode --type creator --creator_id "123456789"

# 微博用户数据
uv run main.py --platform wb --lt qrcode --type creator --creator_id "7797463367"
```

### 场景4: 不同平台爬取

```bash
# 抖音关键词搜索
uv run main.py --platform dy --lt qrcode --type search --keywords "科技"

# 快手关键词搜索
uv run main.py --platform ks --lt qrcode --type search --keywords "游戏"

# B站关键词搜索
uv run main.py --platform bili --lt qrcode --type search --keywords "教程"

# 微博关键词搜索
uv run main.py --platform wb --lt qrcode --type search --keywords "新闻"

# 贴吧关键词搜索
uv run main.py --platform tieba --lt qrcode --type search --keywords "Python"

# 知乎关键词搜索
uv run main.py --platform zhihu --lt qrcode --type search --keywords "编程"
```

### 场景5: 不同存储方式

```bash
# 保存为CSV文件
uv run main.py --platform xhs --lt qrcode --type search --save_data_option csv

# 保存为JSON文件
uv run main.py --platform xhs --lt qrcode --type search --save_data_option json

# 保存为Excel文件
uv run main.py --platform xhs --lt qrcode --type search --save_data_option excel

# 保存到SQLite数据库（推荐，无需额外配置）
uv run main.py --platform xhs --lt qrcode --type search --save_data_option sqlite

# 保存到MySQL数据库（需先配置数据库）
uv run main.py --platform xhs --lt qrcode --type search --save_data_option db

# 保存到PostgreSQL数据库（需先配置数据库）
uv run main.py --platform xhs --lt qrcode --type search --save_data_option postgres

# 保存到MongoDB数据库（需先配置数据库）
uv run main.py --platform xhs --lt qrcode --type search --save_data_option mongodb
```

### 场景6: 初始化数据库

```bash
# 初始化SQLite数据库
uv run main.py --init_db sqlite

# 初始化MySQL数据库
uv run main.py --init_db mysql

# 初始化PostgreSQL数据库
uv run main.py --init_db postgres
```

### 场景7: Cookie登录方式

```bash
# 使用Cookie登录（适用于已有有效Cookie的情况）
uv run main.py --platform xhs --lt cookie --cookies "your_cookie_string" --type search
```

### 场景8: 完整参数组合示例

```bash
# 小红书搜索 + 启用评论 + 保存到数据库 + 显示浏览器
uv run main.py \
  --platform xhs \
  --lt qrcode \
  --type search \
  --keywords "美食,旅游" \
  --get_comment yes \
  --get_sub_comment yes \
  --max_comments_count_singlenotes 50 \
  --save_data_option sqlite \
  --headless no

# 抖音指定视频详情 + 大量评论
uv run main.py \
  --platform dy \
  --lt qrcode \
  --type detail \
  --specified_id "7123456789012345678" \
  --get_comment yes \
  --max_comments_count_singlenotes 200 \
  --save_data_option json
```

---

## 配置文件说明

项目支持通过配置文件预设默认值，避免每次输入冗长的命令行参数。

### 主要配置文件

#### 1. `config/base_config.py` - 基础配置

**重要配置项：**

```python
# 平台选择
PLATFORM = "xhs"  # xhs | dy | ks | bili | wb | tieba | zhihu

# 关键词配置
KEYWORDS = "编程副业,编程兼职"

# 登录方式
LOGIN_TYPE = "qrcode"  # qrcode | phone | cookie

# 爬取类型
CRAWLER_TYPE = "search"  # search | detail | creator

# 无头模式
HEADLESS = False  # False=显示浏览器，True=隐藏浏览器

# 存储方式
SAVE_DATA_OPTION = "json"  # csv | db | json | sqlite | excel | postgres

# 爬取开始页
START_PAGE = 1

# 最大爬取数量
CRAWLER_MAX_NOTES_COUNT = 15

# 是否爬取评论
ENABLE_GET_COMMENTS = False

# 是否爬取二级评论
ENABLE_GET_SUB_COMMENTS = False

# 单个帖子最大评论数
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 10

# 是否启用IP代理
ENABLE_IP_PROXY = False

# CDP模式配置（使用现有浏览器）
ENABLE_CDP_MODE = False
CUSTOM_BROWSER_PATH = ""  # 自定义浏览器路径
CDP_DEBUG_PORT = 9222
```

#### 2. `config/db_config.py` - 数据库配置

**数据库连接配置：**

```python
# MySQL配置
MYSQL_DB_HOST = "localhost"
MYSQL_DB_PORT = 3306
MYSQL_DB_USER = "root"
MYSQL_DB_PWD = "123456"
MYSQL_DB_NAME = "media_crawler"

# SQLite配置
SQLITE_DB_PATH = "database/sqlite_tables.db"

# PostgreSQL配置
POSTGRES_DB_HOST = "localhost"
POSTGRES_DB_PORT = 5432
POSTGRES_DB_USER = "postgres"
POSTGRES_DB_PWD = "postgres"
POSTGRES_DB_NAME = "media_crawler"

# MongoDB配置
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_USER = ""
MONGODB_PWD = ""
MONGODB_DB_NAME = "media_crawler"

# Redis配置（缓存）
REDIS_DB_HOST = "127.0.0.1"
REDIS_DB_PORT = 6379
REDIS_DB_PWD = "123456"
REDIS_DB_NUM = 0
```

#### 3. 各平台特定配置

每个平台都有独立的配置文件，用于配置平台特定的ID列表：

- `config/xhs_config.py` - 小红书配置
- `config/weibo_config.py` - 微博配置
- `config/dy_config.py` - 抖音配置
- `config/bilibili_config.py` - B站配置
- `config/ks_config.py` - 快手配置
- `config/tieba_config.py` - 贴吧配置
- `config/zhihu_config.py` - 知乎配置

**示例（小红书配置）：**
```python
# 排序方式
SORT_TYPE = "popularity_descending"

# 指定笔记URL列表（detail模式使用）
XHS_SPECIFIED_NOTE_URL_LIST = [
    "https://www.xiaohongshu.com/explore/64b95d01000000000c034587?xsec_token=...",
]

# 指定创作者URL列表（creator模式使用）
XHS_CREATOR_ID_LIST = [
    "https://www.xiaohongshu.com/user/profile/6129d00a0000000001002b57?xsec_token=...",
]
```

### 配置优先级

**命令行参数 > 配置文件**

命令行参数会覆盖配置文件中的同名配置。例如：

```bash
# 配置文件中 PLATFORM = "xhs"
# 但命令行指定了 --platform dy
# 实际运行时会使用抖音平台
uv run main.py --platform dy --type search
```

---

## 注意事项

### 1. 法律合规

- 本项目仅供学习和研究使用
- 禁止用于商业用途
- 使用时应遵守目标平台的使用条款
- 不得进行大规模爬取或对平台造成运营干扰
- 应合理控制请求频率，避免给目标平台带来负担

### 2. 登录相关

- **推荐使用扫码登录**（`--lt qrcode`），成功率最高
- 小红书如果一直扫码登录不通过，设置 `--headless no` 打开浏览器手动过滑动验证码
- 抖音如果一直提示失败，打开浏览器看是否扫码后出现手机号验证
- 登录态会保存在 `chrome_user_data/` 目录，下次运行可复用

### 3. 反检测配置

项目支持两种浏览器运行模式：

**普通 Playwright 模式（默认）：**
- 使用 Playwright 启动的独立浏览器实例
- 适合一般爬取需求

**CDP 模式（推荐，反检测更强）：**
在 `config/base_config.py` 中配置：
```python
ENABLE_CDP_MODE = True          # 启用CDP模式
CUSTOM_BROWSER_PATH = ""        # 留空自动检测，或指定浏览器路径
CDP_DEBUG_PORT = 9222           # CDP调试端口
CDP_HEADLESS = False            # CDP模式下的无头设置
```

CDP模式使用用户现有的Chrome/Edge浏览器，提供更好的反检测能力。

### 4. 数据存储建议

- **CSV/JSON/Excel**：适合小量数据和临时分析
- **SQLite**：推荐，无需额外配置，支持数据排重
- **MySQL/PostgreSQL/MongoDB**：适合大量数据和长期存储

### 5. 性能优化

- 合理设置 `CRAWLER_MAX_NOTES_COUNT` 控制爬取数量
- 合理设置 `CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES` 控制评论数量
- 使用 `--start` 参数实现断点续爬
- 启用数据库存储可实现自动去重

### 6. 环境要求

- **Python**: >= 3.11
- **Node.js**: >= 16.0.0（抖音和知乎签名需要）
- **包管理器**: 推荐使用 `uv`，也可使用 `pip`

### 7. 代理IP配置

如需使用代理IP，在 `config/base_config.py` 中配置：

```python
ENABLE_IP_PROXY = True
IP_PROXY_POOL_COUNT = 2
IP_PROXY_PROVIDER_NAME = "kuaidaidai"  # kuaidaidai | wandouhttp
```

### 8. 词云生成

仅当 `--save_data_option json` 时可用，在配置文件中：

```python
ENABLE_GET_WORDCLOUD = True
```

会在爬取完成后自动生成评论词云图。

---

## WebUI 界面

项目提供了 WebUI 可视化界面，无需命令行操作：

```bash
# 启动WebUI服务
uv run uvicorn api.main:app --port 8080 --reload

# 访问地址
http://localhost:8080
```

WebUI 功能：
- 可视化配置爬虫参数
- 实时查看运行状态和日志
- 数据预览和导出

---

## 常见问题

### Q1: 如何查看所有可用参数？

```bash
uv run main.py --help
```

### Q2: 如何同时爬取多个关键词？

使用逗号分隔：
```bash
--keywords "关键词1,关键词2,关键词3"
```

### Q3: 如何批量爬取多个帖子？

使用逗号分隔ID：
```bash
--specified_id "id1,id2,id3"
```

### Q4: 数据保存在哪里？

- **JSON**: `output_data/` 目录
- **CSV**: `output_data/` 目录
- **Excel**: `output_data/` 目录
- **SQLite**: `database/sqlite_tables.db`
- **MySQL**: 配置的数据库中

### Q5: 如何实现断点续爬？

使用 `--start` 参数指定从第几页开始：
```bash
--start 5  # 从第5页继续爬取
```

---

## 技术支持

- **GitHub Issues**: https://github.com/NanmiCoder/MediaCrawler/issues
- **完整文档**: https://nanmicoder.github.io/MediaCrawler/
- **微信交流群**: [点击加入](https://nanmicoder.github.io/MediaCrawler/%E5%BE%AE%E4%BF%A1%E4%BA%A4%E6%B5%81%E7%BE%A4.html)

---

*本文档基于 MediaCrawler 项目代码分析生成，最后更新：2025年*
