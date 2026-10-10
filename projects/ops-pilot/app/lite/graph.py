"""单机轻量诊断图。

图结构：

    route -> retrieve -> collect_evidence -> synthesize -> finalize

它对应原项目的核心思想，但不触碰 Milvus/Redis/PostgreSQL 的启动流程。
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

from app.lite.knowledge import retrieve_local
from app.lite.models import LiteEvidence, LiteState
from app.lite.router import route_query
from app.lite.tools import collect_local_evidence


load_dotenv()


def _route_node(state: LiteState) -> dict[str, Any]:
    skill, reason, plan = route_query(state.get("query", ""))
    return {"skill": skill, "plan": [reason, *plan]}


def _retrieve_node(state: LiteState) -> dict[str, Any]:
    if state.get("skip_rag"):
        return {"degraded": ["本次运行跳过 RAG，仅验证 Agent 状态流转"]}
    try:
        hits = retrieve_local(
            state.get("query", ""),
            max_docs=state.get("max_docs", 80),
            top_k=state.get("top_k", 4),
        )
    except Exception as exc:
        return {
            "degraded": [f"RAG 检索失败，已降级为无知识库诊断: {type(exc).__name__}: {exc}"],
        }

    evidence = [
        LiteEvidence(
            evidence_id=f"E{i}",
            kind="knowledge",
            source=str(hit["source"]),
            content=str(hit["content"]),
            confidence=0.7,
        ).model_dump()
        for i, hit in enumerate(hits, start=1)
    ]
    if not evidence:
        return {"degraded": ["RAG 未返回相关文档"]}
    return {"evidence": evidence}


def _collect_node(state: LiteState) -> dict[str, Any]:
    next_index = len(state.get("evidence", [])) + 1
    snapshot = collect_local_evidence(state.get("skill", "generic_oncall"))
    evidence = LiteEvidence(
        evidence_id=f"E{next_index}",
        kind="tool",
        source=str(snapshot["source"]),
        content=str(snapshot["content"]),
        confidence=float(snapshot["confidence"]),
    )
    return {"evidence": [evidence.model_dump()]}


def _format_evidence(state: LiteState) -> str:
    blocks = []
    for item in state.get("evidence", []):
        blocks.append(
            f"[{item.get('evidence_id')}] 来源: {item.get('source')}\n"
            f"置信度: {item.get('confidence')}\n{item.get('content')}"
        )
    return "\n\n".join(blocks) or "暂无可用证据。"


def _build_llm() -> Any | None:
    provider = os.getenv("LITE_LLM_PROVIDER", "deepseek").lower().strip()
    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("LITE_LOCAL_LLM_MODEL", "deepseek-r1:1.5b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0,
        )

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        return None
    return ChatOpenAI(
        model=os.getenv("LITE_LLM_MODEL", "deepseek-chat"),
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        temperature=0.1,
        max_retries=1,
    )


def _fallback_report(state: LiteState) -> str:
    degraded = state.get("degraded", [])
    degraded_text = "\n".join(f"- {item}" for item in degraded) or "- 无"
    evidence_text = "\n\n".join(
        f"- [{item.get('evidence_id')}] {item.get('source')}: "
        f"{str(item.get('content', ''))[:300]}"
        for item in state.get("evidence", [])
    ) or "- 暂无"
    return (
        "# 轻量故障诊断报告\n\n"
        f"## 故障描述\n{state.get('query', '')}\n\n"
        f"## Skill\n{state.get('skill', 'generic_oncall')}\n\n"
        "## 当前证据\n"
        f"{evidence_text}\n\n"
        "## 降级情况\n"
        f"{degraded_text}\n\n"
        "## 结论\n"
        "当前运行用于验证 Agent 编排和证据收集链路，未在证据不足时强行生成确定性根因。"
    )


async def _synthesize_node(state: LiteState) -> dict[str, Any]:
    llm = _build_llm()
    if llm is None:
        return {"report": _fallback_report(state), "degraded": ["未配置 DeepSeek API，使用确定性报告兜底"]}

    prompt = (
        "你是一个谨慎的 OnCall 故障诊断助手。只能根据给出的证据回答，"
        "不允许编造不存在的监控数据。报告必须引用证据编号，例如 [E1]。\n\n"
        f"故障描述：{state.get('query', '')}\n"
        f"诊断 Skill：{state.get('skill', '')}\n"
        f"排查计划：{state.get('plan', [])}\n"
        f"证据：\n{_format_evidence(state)}\n"
        f"已知降级：{state.get('degraded', [])}\n\n"
        "请输出：现象、证据分析、可能根因、建议动作、信息缺口。"
    )
    try:
        response = await llm.ainvoke(
            [
                SystemMessage(content="输出中文 Markdown，结论要区分事实和推测。"),
                HumanMessage(content=prompt),
            ]
        )
        content = response.content
        if isinstance(content, list):
            content = "".join(str(item) for item in content)
        return {"report": str(content).strip() or _fallback_report(state)}
    except Exception as exc:
        return {
            "report": _fallback_report(state),
            "degraded": [f"LLM 报告生成失败，已回退确定性报告: {type(exc).__name__}: {exc}"],
        }


def _finalize_node(state: LiteState) -> dict[str, Any]:
    report = state.get("report", "")
    if "## 降级情况" not in report:
        report += "\n\n## 降级情况\n" + (
            "\n".join(f"- {item}" for item in state.get("degraded", [])) or "- 无"
        )
    return {"report": report}


def build_lite_graph():
    workflow = StateGraph(LiteState)
    workflow.add_node("route", _route_node)
    workflow.add_node("retrieve", _retrieve_node)
    workflow.add_node("collect_evidence", _collect_node)
    workflow.add_node("synthesize", _synthesize_node)
    workflow.add_node("finalize", _finalize_node)
    workflow.add_edge(START, "route")
    workflow.add_edge("route", "retrieve")
    workflow.add_edge("retrieve", "collect_evidence")
    workflow.add_edge("collect_evidence", "synthesize")
    workflow.add_edge("synthesize", "finalize")
    workflow.add_edge("finalize", END)
    return workflow.compile()


async def run_lite(
    query: str,
    *,
    max_docs: int = 80,
    top_k: int = 4,
    skip_rag: bool = False,
) -> LiteState:
    graph = build_lite_graph()
    return await graph.ainvoke(
        {
            "query": query,
            "max_docs": max_docs,
            "top_k": top_k,
            "skip_rag": skip_rag,
            "evidence": [],
            "degraded": [],
        }
    )
