"""单机轻量运行路径。

保留原项目的 Agent/RAG 设计，但不要求 Milvus、Redis、PostgreSQL 或 Docker。
"""

from app.lite.graph import build_lite_graph, run_lite

__all__ = ["build_lite_graph", "run_lite"]
