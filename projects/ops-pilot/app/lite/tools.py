"""轻量模式的只读本机证据工具。"""

from __future__ import annotations

import platform
import shutil
from pathlib import Path


def collect_local_evidence(skill: str) -> dict[str, str | float]:
    """只收集本机基础信息，不执行修改系统的命令。"""

    # 使用当前工作目录所在的磁盘，避免把开发机盘符写死到公开代码中。
    current_root = Path.cwd().anchor or "."
    disk_usage = shutil.disk_usage(current_root)
    content = (
        f"系统={platform.system()} {platform.release()}\n"
        f"架构={platform.machine()}\n"
        f"Python={platform.python_version()}\n"
        f"当前磁盘可用空间={disk_usage.free / 1024**3:.2f}GB\n"
        f"当前诊断域={skill}\n"
        "说明：轻量模式只采集本机只读快照，不执行重启、删除、修改配置等操作。"
    )
    return {
        "source": "local_read_only_snapshot",
        "content": content,
        "confidence": 0.85,
    }
