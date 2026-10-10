"""命令行入口: python -m app.lite.cli "我电脑最近很卡"""""

from __future__ import annotations

import argparse
import asyncio

from app.lite.graph import run_lite


def main() -> None:
    parser = argparse.ArgumentParser(description="OpsPilot 单机轻量诊断模式")
    parser.add_argument("query", help="故障描述")
    parser.add_argument("--max-docs", type=int, default=80, help="首次索引最多读取多少篇文档")
    parser.add_argument("--top-k", type=int, default=4, help="返回多少条知识证据")
    parser.add_argument("--skip-rag", action="store_true", help="跳过 Embedding/RAG，仅验证图流程")
    args = parser.parse_args()
    state = asyncio.run(
        run_lite(
            args.query,
            max_docs=args.max_docs,
            top_k=args.top_k,
            skip_rag=args.skip_rag,
        )
    )
    print(state.get("report", ""))


if __name__ == "__main__":
    main()
