"""不调用模型的本地自检。适合先确认第七章框架结构没有导入问题。"""

import sys

# Windows 默认 GBK 终端无法输出框架中的中文和符号。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from hello_agents import Message, ToolRegistry
from hello_agents.tools import CalculatorTool


def main() -> None:
    registry = ToolRegistry()
    registry.register_tool(CalculatorTool())

    assert registry.list_tools() == ["python_calculator"]
    assert registry.execute_tool("python_calculator", "2 + 3 * 4") == "14"

    message = Message(content="测试完成", role="assistant")
    assert message.to_dict() == {"role": "assistant", "content": "测试完成"}
    print("本地框架自检通过。")


if __name__ == "__main__":
    main()
