"""轻量诊断图的数据结构。

这里刻意使用显式的 Evidence 记录，而不是只把一段字符串塞进 prompt。
这样后续可以继续扩展成来源、时间、置信度和工具调用的审计链。
"""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from pydantic import BaseModel, Field


class LiteEvidence(BaseModel):
    """一条可追溯证据。"""

    evidence_id: str = Field(description="本次诊断内唯一的证据编号")
    kind: str = Field(description="knowledge 或 tool")
    source: str = Field(description="文档路径、工具名或数据源")
    content: str = Field(description="证据内容")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class LiteState(TypedDict, total=False):
    """单机诊断图的共享状态。"""

    query: str
    skill: str
    plan: list[str]
    evidence: Annotated[list[dict], operator.add]
    degraded: Annotated[list[str], operator.add]
    skip_rag: bool
    top_k: int
    max_docs: int
    report: str
