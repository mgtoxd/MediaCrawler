#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler TUI - Textual Terminal User Interface
一个基于 Textual 框架的终端用户界面，用于配置和管理 MediaCrawler 爬虫
"""

from textual.app import App, ComposeResult
from textual.widgets import (
    Button, Header, Footer, Static, Input,
    DataTable, ListItem, ListView
)
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual import events
from textual.binding import Binding
from textual.screen import ModalScreen
import subprocess
import sys
import os
from pathlib import Path
import re

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class CreatorList(Vertical):
    """Creator ID 列表组件"""

    current_ids = reactive(list)

    def __init__(self, platform_key: str, **kwargs):
        super().__init__(**kwargs)
        self.platform_key = platform_key
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
        self.load_config()

    def load_config(self) -> None:
        """从配置文件加载 CREATOR_ID_LIST"""
        platform_info = self.platforms.get(self.platform_key, {})
        config_file = project_root / platform_info.get("config", "")
        attr_name = platform_info.get("attr", "")

        if not config_file.exists():
            self.creator_ids = []
            return

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()

            pattern = f'{attr_name}\\s*=\\s*\\[(.*?)\\]'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                list_content = match.group(1)
                self.creator_ids = [
                    m.strip().strip('"').strip("'")
                    for m in re.findall(r'["\'][^"\']+["\']', list_content)
                ]
            else:
                self.creator_ids = []

        except Exception as e:
            self.creator_ids = []

    def save_config(self) -> bool:
        """保存 CREATOR_ID_LIST 到配置文件"""
        platform_info = self.platforms.get(self.platform_key, {})
        config_file = project_root / platform_info.get("config", "")
        attr_name = platform_info.get("attr", "")

        if not config_file.exists():
            return False

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()

            if self.creator_ids:
                new_list_items = [f'        "{cid}"' for cid in self.creator_ids]
                new_list_items[-1] = new_list_items[-1].lstrip()
                new_list_content = f"{attr_name} = [\n" + ",\n".join(new_list_items) + "\n    ]"
            else:
                new_list_content = f"{attr_name} = []"

            pattern = f'{attr_name}\\s*=\\s*\\[.*?\\](?=\\n)'
            content = re.sub(pattern, new_list_content, content, flags=re.DOTALL)

            with open(config_file, "w", encoding="utf-8") as f:
                f.write(content)

            return True

        except Exception as e:
            return False

    def add_id(self, creator_id: str) -> None:
        """添加 Creator ID"""
        if creator_id and creator_id not in self.creator_ids:
            self.creator_ids.append(creator_id)
            self.save_config()
            self.update_display()

    def remove_id(self, index: int) -> None:
        """删除 Creator ID"""
        if 0 <= index < len(self.creator_ids):
            removed_id = self.creator_ids[index]
            del self.creator_ids[index]
            self.save_config()
            self.update_display()
            # 显示删除通知
            if hasattr(self, 'app') and self.app:
                self.app.notify(f"🗑️ 已删除: {removed_id}", severity="information")

    def update_display(self) -> None:
        """更新列表显示"""
        table = self.query_one(DataTable)

        # 清除所有内容（行和列）
        table.clear(columns=True)

        # 添加列
        table.add_column("序号", width=6)
        table.add_column("Creator ID", width=60)

        # 添加数据行，使用索引作为行键
        for idx, creator_id in enumerate(self.creator_ids):
            table.add_row(str(idx + 1), creator_id, key=str(idx))

    def on_mount(self) -> None:
        """组件挂载后初始化显示"""
        self.update_display()

    def compose(self) -> ComposeResult:
        """组合 UI 组件"""
        yield DataTable()


class PlatformScreen(ModalScreen):
    """平台配置屏幕"""

    CSS = """
    PlatformScreen {
        align: center middle;
    }

    #platform-dialog {
        width: 90%;
        height: 85%;
        border: thick $primary;
        background: $panel;
        padding: 1;
    }

    #platform-header {
        height: 3;
        margin: 0 0 1 0;
        text-align: center;
        text-style: bold;
        content-align: center middle;
        background: $primary;
    }

    #input-section {
        height: 6;
        margin: 1 0;
    }

    #input-label {
        height: 1;
        margin: 0 0 1 0;
        text-style: bold;
    }

    #creator-input {
        height: 3;
    }

    #list-section {
        height: 1fr;
        margin: 1 0;
    }

    #list-header {
        height: 2;
        margin: 0 0 1 0;
        text-style: bold;
    }

    #list-container {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }

    DataTable {
        height: 100%;
    }

    #button-section {
        height: 4;
        margin: 1 0 0 0;
    }

    .action-button {
        width: 1fr;
        height: 3;
        margin: 0 1;
    }

    Input {
        width: 1fr;
    }
    """

    def __init__(self, platform_key: str, platform_name: str, **kwargs):
        super().__init__(**kwargs)
        self.platform_key = platform_key
        self.platform_name = platform_name

    def compose(self) -> ComposeResult:
        """组合 UI 组件"""
        with Container(id="platform-dialog"):
            yield Static(f"{self.platform_name} - Creator ID 配置", id="platform-header")

            with Vertical(id="input-section"):
                yield Static("➕ 输入 Creator ID 后按 Enter 添加:", id="input-label")
                yield Input(
                    placeholder="纯ID或完整URL，如: 6129d00a0000000001002b57",
                    id="creator-input",
                    value=""
                )

            with Vertical(id="list-section"):
                yield Static("📋 已添加的列表 (选中行后按 Delete 键删除):", id="list-header")
                with Vertical(id="list-container"):
                    yield CreatorList(self.platform_key, id="creator-list")

            with Horizontal(id="button-section"):
                yield Button("◀ 返回", id="close-button", variant="default", classes="action-button")
                yield Button("▶ 运行爬虫", id="run-button", variant="success", classes="action-button")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """处理输入提交"""
        input_widget = self.query_one("#creator-input", Input)
        creator_id = input_widget.value.strip()

        if creator_id:
            creator_list = self.query_one("#creator-list", CreatorList)
            creator_list.add_id(creator_id)
            input_widget.value = ""
            self.notify(f"✅ 已添加: {creator_id}", severity="information")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        if event.button.id == "close-button":
            self.app.pop_screen()
        elif event.button.id == "run-button":
            self.run_crawler()

    def run_crawler(self) -> None:
        """运行爬虫命令"""
        command = [
            "uv", "run", "main.py",
            "--platform", self.platform_key,
            "--lt", "qrcode",
            "--type", "creator",
            "--save_data_option", "postgres"
        ]

        try:
            process = subprocess.Popen(
                command,
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.app.notify(
                title="爬虫已启动",
                message=f"平台: {self.platform_name}\nPID: {process.pid}\n命令: {' '.join(command)}",
                severity="information"
            )
        except Exception as e:
            self.app.notify(
                title="启动失败",
                message=str(e),
                severity="error"
            )


class MediaCrawlerTUI(App):
    """MediaCrawler TUI 主应用"""

    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("r", "refresh", "刷新"),
        Binding("delete,backspace", "delete_selected", "删除选中项"),
    ]

    def action_delete_selected(self) -> None:
        """删除选中的行"""
        try:
            # 查找 CreatorList
            creator_list = self.query_one("#creator-list", CreatorList)

            # 查找 DataTable（在 CreatorList 内部）
            table = creator_list.query_one(DataTable)

            # 检查是否有选中的行
            if table.cursor_row is not None:
                # 获取选中行的键
                selected_row_key = table.get_row_at(table.cursor_row).key

                if selected_row_key is not None:
                    # 行键是索引的字符串形式
                    index = int(selected_row_key)

                    # 删除
                    creator_list.remove_id(index)
            else:
                self.notify("请先用方向键选中要删除的行", severity="warning")

        except Exception as e:
            # 如果出错，显示错误信息
            import traceback
            error_msg = f"删除失败: {str(e)}\n{traceback.format_exc()}"
            self.notify(f"删除失败，请确保已选中一行", severity="error")

    CSS = """
    Screen {
        layout: vertical;
    }

    #title {
        text-style: bold;
        text-align: center;
        height: 3;
        margin: 1 0;
        content-align: center middle;
    }

    #menu {
        height: auto;
        margin: 1 2;
    }

    Horizontal {
        height: 3;
        margin: 0 0 1 0;
    }

    Button {
        width: 1fr;
        margin: 0 1;
        min-height: 1;
    }

    #info {
        height: 3;
        margin: 1 2;
        text-style: italic;
    }

    #footer-info {
        height: 3;
        dock: bottom;
        background: $panel;
        padding: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        """组合 UI 组件"""
        yield Header()
        yield Static("MediaCrawler TUI - 平台配置管理", id="title")
        yield Vertical(
            Horizontal(
                Button("小红书", id="btn-xhs", variant="primary"),
                Button("抖音", id="btn-dy", variant="primary"),
            ),
            Horizontal(
                Button("快手", id="btn-ks", variant="primary"),
                Button("B站", id="btn-bili", variant="primary"),
            ),
            Horizontal(
                Button("微博", id="btn-wb", variant="primary"),
                Button("贴吧", id="btn-tieba", variant="primary"),
            ),
            Horizontal(
                Button("知乎", id="btn-zhihu", variant="primary"),
            ),
            id="menu"
        )
        yield Static(
            "📌 使用流程: 点击平台按钮 → 输入 Creator ID → Enter 添加 → 选中行按 Delete 删除 → 点击'运行爬虫'",
            id="info"
        )
        yield Static("快捷键: [Q]退出 | [R]刷新 | [Delete]删除选中项", id="footer-info")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        platforms = {
            "btn-xhs": ("xhs", "小红书"),
            "btn-dy": ("dy", "抖音"),
            "btn-ks": ("ks", "快手"),
            "btn-bili": ("bili", "B站"),
            "btn-wb": ("wb", "微博"),
            "btn-tieba": ("tieba", "贴吧"),
            "btn-zhihu": ("zhihu", "知乎"),
        }

        if event.button.id in platforms:
            platform_key, platform_name = platforms[event.button.id]
            self.push_screen(PlatformScreen(platform_key, platform_name))

    def action_refresh(self) -> None:
        """刷新配置"""
        self.notify("配置已刷新", severity="information")


def main():
    """主函数"""
    app = MediaCrawlerTUI()
    app.run()


if __name__ == "__main__":
    main()
