#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler TUI 启动脚本
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from TUI.app import main

if __name__ == "__main__":
    main()
