"""轻量模式的 Skill Router。

完整项目使用 LLM 做 Skill 选择并通过代码校验结果。
轻量模式先使用确定性关键词路由，保证没有 API Key 时也能验证图编排；
后续接入 DeepSeek 后，可以把这里替换为 LLM Router，而不改变下游状态结构。
"""

from __future__ import annotations


_RULES: dict[str, tuple[str, ...]] = {
    "host_resource_diagnosis": (
        "电脑", "笔记本", "本机", "host", "laptop", "computer", "cpu", "memory", "disk",
        "内存", "磁盘", "卡顿", "slow", "pressure", "oom", "负载", "load",
    ),
    "network_diagnosis": (
        "网络", "网站", "接口", "network", "website", "endpoint", "超时", "timeout", "dns", "端口",
        "port", "连接", "connection", "打不开", "unreachable", "502", "503", "504",
    ),
    "container_diagnosis": (
        "docker", "容器", "镜像", "container", "image", "restart loop", "milvus", "redis", "postgres",
    ),
}


def route_query(query: str) -> tuple[str, str, list[str]]:
    """返回 skill、路由原因和可解释的初始排查计划。"""

    text = (query or "").lower()
    scores = {
        name: sum(1 for keyword in keywords if keyword in text)
        for name, keywords in _RULES.items()
    }
    selected = max(scores, key=scores.get) if scores else "generic_oncall"
    if scores.get(selected, 0) == 0:
        selected = "generic_oncall"
        reason = "未命中专属故障域，使用通用 OnCall 兜底"
    else:
        reason = f"关键词路由命中 {selected}，分数={scores[selected]}"

    plans = {
        "host_resource_diagnosis": ["确认资源异常类型", "检索相关告警和 SOP", "采集本机只读证据", "输出带引用的诊断报告"],
        "network_diagnosis": ["确认目标和异常现象", "检索网络故障 SOP", "整理可执行的连通性检查", "输出带引用的诊断报告"],
        "container_diagnosis": ["确认容器和服务范围", "检索容器故障 SOP", "整理容器状态检查项", "输出带引用的诊断报告"],
        "generic_oncall": ["明确故障边界", "检索相关 SOP", "收集有限的本地证据", "输出信息不足时的下一步建议"],
    }
    return selected, reason, plans[selected]
