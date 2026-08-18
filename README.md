# AI 应用工程学习与项目记录

这是我的 AI 应用工程学习档案与项目展示仓库，记录学习时间、阶段目标、技术实践、代码改动和阶段性成果。

当前主线是 Python + 大模型应用工程，重点学习 Agent、RAG、工作流、工具调用、上下文管理和工程部署。后续会根据实习、课题组任务和实际项目需要，继续补充 FastAPI、MySQL、Docker、评测、可观测性，以及模型部署和推理相关能力。

本仓库不是课程代码压缩包，也不是把照着教程运行过的内容包装成独立项目。仓库中的内容会尽量标明来源、改动范围、掌握程度和当前局限，便于持续追溯。

## 个人方向概览

| 项目 | 内容 |
| --- | --- |
| 当前阶段 | 南京农业大学计算机技术方向，研究生入学前后持续学习 |
| 目标方向 | Python AI 应用工程、Agent / RAG 开发，后续根据实践考虑 AI Infra |
| 当前重点 | 看懂系统架构、数据流和模块职责，完成有意义的二次开发 |
| 学习方式 | 先建立技术全景，再围绕真实项目深入实现、测试和部署 |
| 代码原则 | 不上传密钥、课程原包、个人路径、模型文件或隐私数据 |

## 学习与实践进度

| 时间 | 阶段 | 学习与产出 |
| --- | --- | --- |
| 2026 年 7 月 | LangChain 基础 | 学习模型调用、Prompt、Chain、结构化输出、RAG 基础和工具调用 |
| 2026 年 7 月 | Agent 入门 | 完成 Hello Agents 第一章，理解 Agent、PEAS、ReAct、工具、记忆和终止边界 |
| 2026 年 8 月初 | 大模型与 Agent 扫盲 | 快速学习 Agent 发展背景、大模型能力边界、Token、上下文、Prompt、采样和幻觉 |
| 2026 年 8 月 | LangGraph | 学习 State、Node、Edge、Checkpoint，并完成固定搜索 Workflow 改编 |
| 后续 | 项目工程化 | 根据项目需要补充 RAG 二次开发、FastAPI、MySQL、Docker、评测和部署 |

## 当前可展示内容

### 1. ReAct 旅行助手：课程改编练习

目录：[hello_agent_study/chapter01_react_travel_agent](hello_agent_study/chapter01_react_travel_agent)

在 Hello Agents 示例基础上，保留手写 Thought-Action-Observation 循环，完成了配置脱敏、路径适配、工具注册、异常处理和 Action 解析调整。

可以说明的内容包括：大模型如何决定下一步行动、工具如何被注册和调用、Observation 如何回传、为什么需要循环上限，以及正则解析方案的局限。

### 2. LangGraph 搜索问答：框架学习改编

目录：[hello_agent_study/chapter06_langgraph_search](hello_agent_study/chapter06_langgraph_search)

使用 LangGraph 将“理解问题 → 搜索资料 → 组织回答”拆成固定节点，学习 State、Node、Edge、消息追加和内存检查点。

这个示例明确标注为 Workflow，而不是动态 ReAct Agent，重点展示固定流程和动态 Agent 的区别。

## 仓库结构

    hello_agent_study/
        Hello Agents 课程精选改编与学习说明
    docs/
        学习日志和阶段记录
    projects/
        后续独立项目或有实质改动的项目

## 如何运行示例

1. 准备自己的 Python 环境。当前学习环境原则上使用 agent_study_env。
2. 将 .env.example 复制为根目录的 .env，并填写自己的模型和搜索服务配置。
3. 进入对应示例目录，安装该目录的 requirements.txt。
4. 根据子目录 README 运行 Python 文件。

真实配置文件 .env 已被 Git 忽略，禁止把 API Key 提交到仓库。

## 后续规划

- 继续学习 LangGraph，并结合 learn-claude-code 理解 Agent Harness 和工程机制。
- 选择合适的成熟 RAG / Agent 项目进行架构分析和二次开发。
- 根据真实需求补齐 FastAPI、MySQL、Docker、评测和可观测性。
- 结合课题组和实习机会，在 AI 应用工程与 AI Infra 之间确定下一阶段深化方向。

## 课程来源说明

hello_agent_study 中的内容基于 Datawhale Hello Agents，属于学习改编，不代表独立原创项目。具体来源、改动和许可说明见 [hello_agent_study/README.md](hello_agent_study/README.md) 和 [hello_agent_study/LICENSE.md](hello_agent_study/LICENSE.md)。
