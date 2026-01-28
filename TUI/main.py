#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler TUI - Textual Terminal User Interface
一个基于 Textual 框架的终端用户界面，用于配置和管理 MediaCrawler 爬虫
"""

from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, Input, ListItem, ListView
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual import events
import subprocess
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class PlatformConfig(Static):
    """平台配置组件"""

    current_platform = reactive("xhs")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.platforms = {
            "xhs": {"name": "小红书", "config": "config/xhs_config.py", "attr": "XHS_CREATOR_ID_LIST"},
            "dy": {"name": "抖音", "config": "config/dy_config.py", "attr": "DY_CREATOR_ID_LIST"},
            "ks": {"name": "快手", "config": "config/ks_config.py", "attr": "KS_CREATOR_ID_LIST"},
            "bili": {"name": "B站", "config": "config/bilibili_config.py", "attr": "BILIBILI_CREATOR_ID_LIST"},
            "wb": {"name": "微博", "config": "config/weibo_config.py", "attr": "WEIBO_CREATOR_ID_LIST"},
            "tieba": {"name": "贴吧", "config": "config/tieba_config.py", "attr": "TIEBA_CREATOR_ID_LIST"},
            "zhihu": {"name": "知乎", "config": "config/zhihu_config.py", "attr": "ZHIHU_CREATOR_ID_LIST"},
        }
        self.creator_ids = []

    def watch_current_platform(self, old_platform: str, new_platform: str) -> None:
        """当平台改变时重新加载配置"""
        if new_platform:
            self.load_config()

    def load_config(self) -> None:
        """从配置文件加载 CREATOR_ID_LIST"""
        platform_info = self.platforms.get(self.current_platform, {})
        config_file = project_root / platform_info.get("config", "")
        attr_name = platform_info.get("attr", "")

        if not config_file.exists():
            self.creator_ids = []
            return

        try:
            # 读取配置文件
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 使用正则表达式提取 CREATOR_ID_LIST
            import re
            pattern = f'{attr_name}\\s*=\\s*\\[(.*?)\\]'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                list_content = match.group(1)
                # 提取所有字符串
                self.creator_ids = re.findall(r'["\']([^"\']+)["\']', list_content)
            else:
                self.creator_ids = []

        except Exception as e:
            self.creator_ids = []

    def save_config(self) -> bool:
        """保存 CREATOR_ID_LIST 到配置文件"""
        platform_info = self.platforms.get(self.current_platform, {})
        config_file = project_root / platform_info.get("config", "")
        attr_name = platform_info.get("attr", "")

        if not config_file.exists():
            return False

        try:
            # 读取配置文件
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 构建新的列表内容
            if self.creator_ids:
                new_list = "\n    ".join([f'"{cid}"' if i == len(self.creator_ids) - 1 else f'        "{cid}",'
                                          for i, cid in enumerate(self.creator_ids)])
                new_list_content = f"{attr_name} = [\n    {new_list}\n]"
            else:
                new_list_content = f"{attr_name} = []"

            # 替换配置
            import re
            pattern = f'{attr_name}\\s*=\\s*\\[.*?\\]\\n'
            content = re.sub(pattern, new_list_content + "\n", content, flags=re.DOTALL)

            # 写回文件
            with open(config_file, "w", encoding="utf-8") as f:
                f.write(content)

            return True

        except Exception as e:
            return False

    def compose(self) -> ComposeResult:
        """组合 UI 组件"""
        yield Static(f"当前平台: {self.platforms.get(self.current_platform, {}).get('name', '')}", id="platform-title")
        yield Static("Creator ID 列表 (每行一个，按 Enter 添加):", id="label")
        yield Input(placeholder="输入 Creator ID 后按 Enter 添加", id="creator-input")
        yield Static("已添加的 Creator IDs (点击删除):", id="list-label")
        yield Vertical(id="creator-list")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """处理输入提交"""
        input_widget = self.query_one("#creator-input", Input)
        creator_id = input_widget.value.strip()

        if creator_id and creator_id not in self.creator_ids:
            self.creator_ids.append(creator_id)
            self.save_config()
            self.update_list()

        input_widget.value = ""

    def update_list(self) -> None:
        """更新列表显示"""
        list_container = self.query_one("#creator-list", Vertical)
        list_container.remove_children()

        for creator_id in self.creator_ids:
            item = ListItem(
                Button(creator_id, id=f"remove-{self.creator_ids.index(creator_id)}"),
                classes="creator-item"
            )
            list_container.mount(item)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        if event.button.id.startswith("remove-"):
            index = int(event.button.id.split("-")[1])
            if 0 <= index < len(self.creator_ids):
                del self.creator_ids[index]
                self.save_config()
                self.update_list()


class MediaCrawlerTUI(App):
    """MediaCrawler TUI 主应用"""

    CSS = """
    Screen {
        layout: vertical;
    }

    #menu {
        height: 3;
        dock: top;
    }

    Horizontal {
        height: 3;
    }

    Button {
        width: 1fr;
        margin: 0 1;
    }

    #config-container {
        height: 1fr;
        padding: 1;
    }

    #platform-title {
        text-style: bold;
        margin: 1 0;
        text-align: center;
    }

    #label, #list-label {
        margin: 1 0;
        text-style: italic;
    }

    #creator-input {
        margin: 1 0;
    }

    #creator-list {
        height: 1fr;
        border: solid green;
        padding: 1;
        overflow: y;
    }

    .creator-item {
        height: 1;
    }

    .creator-item Button {
        width: 1fr;
    }

    #run-container {
        height: 3;
        dock: bottom;
    }

    #run-button {
        width: 1fr;
    }

    #status {
        height: 3;
        dock: bottom;
        background: $panel;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        """组合 UI 组件"""
        yield Header()
        yield Horizontal(
            Button("小红书", id="btn-xhs", variant="primary"),
            Button("抖音", id="btn-dy", variant="primary"),
            Button("快手", id="btn-ks", variant="primary"),
            Button("B站", id="btn-bili", variant="primary"),
            Button("微博", id="btn-wb", variant="primary"),
            Button("贴吧", id="btn-tieba", variant="primary"),
            Button("知乎", id="btn-zhihu", variant="primary"),
            id="menu"
        )
        yield PlatformConfig(id="config-container")
        yield Horizontal(
            Button("运行爬虫", id="run-button", variant="success"),
            id="run-container"
        )
        yield Static("准备就绪", id="status")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        config = self.query_one("#config-container", PlatformConfig)

        if event.button.id.startswith("btn-"):
            # 平台按钮
            platform = event.button.id.replace("btn-", "")
            config.current_platform = platform
            config.update_list()
            self.update_status(f"已切换到 {config.platforms.get(platform, {}).get('name', platform)} 平台")

        elif event.button.id == "run-button":
            # 运行爬虫
            self.run_crawler()

    def update_status(self, message: str) -> None:
        """更新状态栏"""
        status = self.query_one("#status", Static)
        status.update(message)

    def run_crawler(self) -> None:
        """运行爬虫命令"""
        config = self.query_one("#config-container", PlatformConfig)
        platform = config.current_platform

        # 构建命令
        command = [
            "uv", "run", "main.py",
            "--platform", platform,
            "--lt", "qrcode",
            "--type", "creator",
            "--save_data_option", "postgres"
        ]

        # 更新状态
        self.update_status(f"正在运行: {' '.join(command)}")

        try:
            # 在后台运行命令
            process = subprocess.Popen(
                command,
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.update_status(f"爬虫已启动 (PID: {process.pid})，请查看终端输出")

        except Exception as e:
            self.update_status(f"启动失败: {str(e)}")


def main():
    """主函数"""
    app = MediaCrawlerTUI()
    app.run()


if __name__ == "__main__":
    main()
