# HelloAgents 第七章：自建 Agent 框架改编版

这是 Datawhale `hello-agents` 第七章的学习改编。目标不是重新发布一个通用框架，而是通过阅读和改写源码，理解 Agent 框架内部的模型接口、Agent 抽象、工具注册和典型 Agent 范式。

## 目录结构

```text
chapter07_helloagents_framework/
├── hello_agents/           # 第七章自己构建的框架源码
│   ├── core/               # LLM、Agent 基类、Message、Config
│   ├── agents/             # Simple、ReAct、Reflection、Plan-and-Solve
│   └── tools/              # Tool、ToolRegistry、工具链、异步工具执行器
├── my_llm.py               # 你的 API 配置适配层
├── my_react_agent.py       # 第七章 ReAct 改写示例
├── my_simple_agent.py      # 支持文本工具调用的 SimpleAgent 改写示例
├── my_calculator_tool.py   # 自定义计算器工具
├── my_advanced_search.py   # 可选的 Tavily/SerpAPI 多源搜索工具
├── run_demo.py             # 推荐入口
├── test_local_framework.py # 不调用模型的本地自检
└── .env.example            # 配置模板
```

## 第一次运行

在 Anaconda Prompt 或终端中执行：

```powershell
conda activate agent_study_env
cd hello_agent_study\chapter07_helloagents_framework
python test_local_framework.py
python run_demo.py
```

默认的 `run_demo.py` 只测试本地计算器、工具注册表和消息对象，不调用 API。

## 调用模型

1. 将 `.env.example` 复制为同目录的 `.env`。
2. 填写 `GUAIHUB_MODEL`、`GUAIHUB_API_KEY`、`GUAIHUB_BASE_URL`。
3. 不要把 `.env` 上传到 GitHub。

例如：

```dotenv
GUAIHUB_MODEL=deepseek-chat
GUAIHUB_API_KEY=你的Key
GUAIHUB_BASE_URL=https://你的中转站地址/v1
```

然后运行：

```powershell
python run_demo.py simple
python run_demo.py react
python run_demo.py reflection
python run_demo.py plan
```

## 本章要理解的主线

```text
HelloAgentsLLM
    ↓ 统一模型调用接口
Agent 基类
    ↓ 规定 run() 和历史记录能力
具体 Agent 范式
    ├── SimpleAgent
    ├── ReActAgent
    ├── ReflectionAgent
    └── PlanAndSolveAgent
工具系统
    ├── Tool
    ├── ToolRegistry
    ├── ToolChain
    └── AsyncToolExecutor
```

本章重点不是记住所有类，而是看懂三种抽象：

1. **统一模型接口**：不同模型服务都通过 `HelloAgentsLLM.invoke()` / `think()` 调用。
2. **Agent 基类和继承**：不同 Agent 复用名称、模型、配置、历史记录等通用能力。
3. **统一工具接口和注册表**：Agent 不需要知道工具内部细节，只需要通过工具名查找并执行。

## 与 LangChain/LangGraph 的关系

这一章是在手写一个教学版 Agent 框架：

- LangChain 把模型、Prompt、Retriever、Tool 等组件封装好；
- LangGraph 把状态、节点、边和循环组织好；
- HelloAgents 则把 Agent、消息、工具注册和几种 Agent 范式的核心逻辑直接写出来。

因此，学习本章的价值是理解“框架内部到底替你做了什么”，不是以后必须放弃 LangChain/LangGraph 改用这个教学框架。

## 本次改写内容

- 将课程依赖的 `hello_agents` 框架源码放入当前目录，解决示例单独下载后无法导入的问题。
- 使用 `my_llm.py` 替代老师示例中的 ModelScope 配置，支持你的 DeepSeek/OpenAI 兼容 API。
- 同时兼容 `GUAIHUB_*`、`DEEPSEEK_*` 和标准 `LLM_*` 环境变量命名。
- 增加 `run_demo.py`，默认执行不产生费用的本地检查；只有显式选择 Agent 模式才调用模型。
- 保留计算器、ReAct、SimpleAgent 和高级搜索示例，搜索 Key 仍然是可选配置。
- 增加中文说明、最小依赖清单和本地框架自检。

## 重要边界

这是课程学习框架，不是生产级 Agent 框架。它使用文本格式解析 ReAct 工具调用，真实项目中应进一步增加结构化输出、权限控制、工具参数校验、持久化记忆、日志追踪和评测。
