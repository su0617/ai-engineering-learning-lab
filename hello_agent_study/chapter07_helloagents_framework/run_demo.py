"""第七章最小可运行入口。

默认只运行本地计算器，不调用模型；传入模式后才会调用 API：

    python run_demo.py simple
    python run_demo.py react
    python run_demo.py reflection
    python run_demo.py plan
"""

import sys
from pathlib import Path

# Windows 默认 GBK 终端无法输出框架中的中文和符号，统一切到 UTF-8。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

from my_calculator_tool import create_calculator_registry


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


def run_local_check() -> None:
    """验证框架导入、工具注册和本地工具执行，不产生 API 费用。"""
    
    from hello_agents import Message

    registry = create_calculator_registry()
    print("可用工具:", registry.list_tools())
    print("2 + 3 * 4 =", registry.execute_tool("my_calculator", "2 + 3 * 4"))
    print("消息对象:", Message(content="本地检查完成", role="assistant").to_dict())


def build_llm():
    """延迟创建模型，保证本地检查不需要填写 API。"""

    from my_llm import MyLLM

    return MyLLM()


def run_model_demo(mode: str) -> None:
    """运行一个第七章 Agent 范式示例。"""

    llm = build_llm()
    question = "请用三句话解释为什么 Agent 需要工具，并举一个物流场景例子。"

    if mode == "simple":
        from hello_agents import SimpleAgent

        agent = SimpleAgent(
            name="简单对话助手",
            llm=llm,
            system_prompt="你是一个简洁、准确的中文学习助手。",
        )
    elif mode == "react":
        from my_react_agent import MyReActAgent

        agent = MyReActAgent(
            name="ReAct学习助手",
            llm=llm,
            tool_registry=create_calculator_registry(),
            max_steps=3,
        )
        question = "请计算 (25 + 15) * 3 - 8，并解释计算结果。"
    elif mode == "reflection":
        from hello_agents import ReflectionAgent

        agent = ReflectionAgent(name="反思学习助手", llm=llm, max_iterations=1)
    elif mode == "plan":
        from hello_agents import PlanAndSolveAgent

        agent = PlanAndSolveAgent(name="规划学习助手", llm=llm)
    else:
        raise ValueError(f"不支持的模式: {mode}")

    print(f"\n开始运行 {mode} 模式...\n")
    print(agent.run(question))


if __name__ == "__main__":
    selected_mode = sys.argv[1].lower() if len(sys.argv) > 1 else "local"
    if selected_mode == "local":
        run_local_check()
    else:
        run_model_demo(selected_mode)
