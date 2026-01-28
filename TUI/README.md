# MediaCrawler TUI

一个基于 Textual 框架的终端用户界面（TUI），用于简化 MediaCrawler 爬虫的配置和运行。

## 功能特性

- 🎯 **可视化配置** - 通过图形界面配置各平台的 Creator ID
- ⚡ **即时保存** - 修改配置后立即写入到对应的配置文件
- 🚀 **一键运行** - 直接在界面中启动爬虫任务
- 📋 **列表管理** - 轻松添加、删除 Creator IDs

## 支持的平台

- 小红书 (xhs)
- 抖音 (dy)
- 快手 (ks)
- B站 (bili)
- 微博 (wb)
- 贴吧 (tieba)
- 知乎 (zhihu)

## 安装依赖

首先确保已安装 Textual 框架：

```bash
uv pip install textual
```

或者使用 pip：

```bash
pip install textual
```

## 使用方法

### 方式一：直接运行

```bash
cd TUI
python run.py
```

### 方式二：从项目根目录运行

```bash
python TUI/run.py
```

### 方式三：作为模块运行

```bash
python -m TUI.app
```

## 操作指南

### 主界面

主界面显示 7 个平台按钮，点击任意按钮进入该平台的配置界面。

### 配置界面

1. **添加 Creator ID**
   - 在输入框中输入 Creator ID
   - 按 Enter 键添加到列表

2. **删除 Creator ID**
   - 点击列表中的任意行即可删除对应的 ID

3. **运行爬虫**
   - 点击"运行爬虫"按钮
   - 爬虫将在后台启动
   - 使用命令：`uv run main.py --platform <平台> --lt qrcode --type creator --save_data_option postgres`

4. **返回主界面**
   - 点击"返回"按钮

### 快捷键

- `Q` - 退出程序
- `R` - 刷新配置

## 配置文件

程序会修改以下配置文件：

- `config/xhs_config.py` - 小红书配置
- `config/dy_config.py` - 抖音配置
- `config/ks_config.py` - 快手配置
- `config/bilibili_config.py` - B站配置
- `config/weibo_config.py` - 微博配置
- `config/tieba_config.py` - 贴吧配置
- `config/zhihu_config.py` - 知乎配置

修改的配置项为各平台对应的 `*_CREATOR_ID_LIST` 属性。

## 注意事项

1. **配置备份** - 修改配置前建议备份原配置文件
2. **爬虫运行** - 爬虫在后台运行，输出会显示在启动的终端中
3. **登录方式** - 默认使用扫码登录 (`--lt qrcode`)
4. **存储方式** - 默认使用 PostgreSQL (`--save_data_option postgres`)，可在代码中修改

## 自定义配置

### 修改默认命令

编辑 `TUI/app.py` 文件中的 `run_crawler` 方法：

```python
def run_crawler(self) -> None:
    """运行爬虫命令"""
    command = [
        "uv", "run", "main.py",
        "--platform", self.platform_key,
        "--lt", "qrcode",  # 修改登录方式
        "--type", "creator",
        "--save_data_option", "sqlite"  # 修改存储方式
    ]
```

### 添加更多平台

1. 在 `platforms` 字典中添加新平台
2. 确保对应的配置文件存在
3. 在主界面添加新按钮

## 故障排除

### 问题：无法启动

确保：
- 已安装 Textual 框架
- Python 版本 >= 3.11
- 在项目根目录下运行

### 问题：配置未保存

检查：
- 配置文件是否存在
- 文件是否有写入权限
- 配置文件格式是否正确

### 问题：爬虫启动失败

确认：
- `uv` 命令是否可用
- 项目依赖是否已安装
- 配置文件是否正确

## 开发计划

- [ ] 支持配置更多参数（关键词、爬取数量等）
- [ ] 显示爬虫运行状态
- [ ] 查看爬虫日志
- [ ] 支持多个爬虫任务并发运行
- [ ] 配置导入/导出功能

## 许可证

本项目遵循 MediaCrawler 主项目的许可证。
