"""适配 DeepSeek 或其他 OpenAI 兼容中转站的 LLM 客户端。"""

import os
from typing import Optional

from hello_agents import HelloAgentsLLM


def _first_env(*names: str) -> Optional[str]:
    """按顺序读取第一个非空环境变量，兼容课程和个人配置命名。"""

    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


class MyLLM(HelloAgentsLLM):
    """使用你的 DeepSeek API 配置，同时保留父类统一调用接口。"""

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        # 兼容你之前使用的 GUAIHUB_* 命名，也支持标准 LLM_* 命名。
        resolved_model = model or _first_env(
            "GUAIHUB_MODEL", "DEEPSEEK_MODEL", "LLM_MODEL_ID"
        )
        resolved_key = api_key or _first_env(
            "GUAIHUB_API_KEY", "DEEPSEEK_API_KEY", "LLM_API_KEY"
        )
        resolved_base_url = base_url or _first_env(
            "GUAIHUB_BASE_URL", "DEEPSEEK_BASE_URL", "LLM_BASE_URL"
        )

        if not resolved_model or not resolved_key or not resolved_base_url:
            raise ValueError(
                "缺少模型配置，请在 self_agent/.env 中填写 "
                "GUAIHUB_MODEL、GUAIHUB_API_KEY、GUAIHUB_BASE_URL。"
            )

        # DeepSeek 官方和多数中转站都兼容 OpenAI Chat Completions 接口。
        super().__init__(
            model=resolved_model,
            api_key=resolved_key,
            base_url=resolved_base_url,
            provider="deepseek",
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            max_tokens=kwargs.pop("max_tokens", None),
            timeout=int(os.getenv("LLM_TIMEOUT", "60")),
            **kwargs,
        )
