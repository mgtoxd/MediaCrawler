# MediaCrawler TUI - 快速开始

## 一分钟快速上手

### 1. 安装依赖
```bash
uv pip install textual
```

### 2. 运行程序
```bash
python TUI/run.py
```

### 3. 使用界面
- 点击平台按钮（如"小红书"）
- 输入 Creator ID，按 Enter 添加
- 点击"运行爬虫"开始任务

## 完整示例

### 配置小红书创作者

```bash
# 1. 启动 TUI
python TUI/run.py

# 2. 点击"小红书"按钮

# 3. 输入 Creator ID
# 输入: 6129d00a0000000001002b57
# 按 Enter

# 4. 添加更多 ID
# 输入: https://www.xiaohongshu.com/user/profile/...
# 按 Enter

# 5. 运行爬虫
# 点击"运行爬虫"按钮
```

### 运行的命令
```bash
uv run main.py --platform xhs --lt qrcode --type creator --save_data_option postgres
```

## 支持的平台

| 按钮 | 平台代码 | 配置文件 |
|------|----------|----------|
| 小红书 | xhs | config/xhs_config.py |
| 抖音 | dy | config/dy_config.py |
| 快手 | ks | config/ks_config.py |
| B站 | bili | config/bilibili_config.py |
| 微博 | wb | config/weibo_config.py |
| 贴吧 | tieba | config/tieba_config.py |
| 知乎 | zhihu | config/zhihu_config.py |

## 快捷键

- `Q` - 退出程序
- `R` - 刷新配置

## 故障排除

### 问题：ModuleNotFoundError: No module named 'textual'

**解决方案：**
```bash
uv pip install textual
```

### 问题：无法保存配置

**检查：**
1. 配置文件是否存在
2. 是否有写入权限
3. 配置文件格式是否正确

### 问题：爬虫启动失败

**检查：**
1. `uv` 命令是否可用
2. 是否在项目根目录运行
3. 依赖是否已安装

## 下一步

- 📖 阅读 [README.md](README.md) 了解详细功能
- 🎨 查看 [demo.md](demo.md) 了解界面布局
- 📝 查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史
