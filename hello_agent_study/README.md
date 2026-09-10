# Hello Agents 学习改编

本目录记录 Datawhale `Hello-Agents` 课程中与 Agent 应用工程直接相关的代码改编，重点覆盖 ReAct、LangGraph、自建 Agent 框架、Memory 和 RAG。

## 项目目录

| 目录 | 时间 | 技术内容 |
| --- | --- | --- |
| `chapter01_react_travel_agent` | 2026-07 | 手写 ReAct 旅行助手、工具注册和执行循环 |
| `chapter06_langgraph_search` | 2026-08 | LangGraph State、Node、Edge 和搜索 Workflow |
| `chapter07_helloagents_framework` | 2026-08 | Agent 基类、Simple/ReAct/Reflection/Plan-and-Solve、ToolRegistry |
| `chapter08_memory_and_rag` | 2026-08 | Memory、RAG、向量检索、工具集成和文档问答 |
| `chapter9` | 2026-09 | ContextBuilder、Memory/Note/Terminal 工具和代码库维护助手 |

## 技术栈

- Python
- DeepSeek/OpenAI 兼容 API
- LangChain / LangGraph
- HelloAgents
- ReAct Agent
- RAG 与 Embedding
- Qdrant / Neo4j（按需启用）
- Gradio（综合 Web 示例）
- Docker、FastAPI、MySQL 等工程化内容将在后续项目中补充

## 代码说明

这些目录是课程代码的学习改编，不是课程原始压缩包，也不宣称为独立生产项目。每个目录尽量保留原始技术主线，并补充：

- DeepSeek/OpenAI 兼容接口配置；
- 环境变量模板；
- 必要的异常处理和运行边界；
- 面向代码阅读的注释；
- 项目 README、运行说明和改动记录。

## 安全与仓库规范

- 不提交真实 API Key、`.env`、个人绝对路径和模型文件；
- 本地知识库、数据库文件、运行报告和缓存均由 `.gitignore` 忽略；
- 大型依赖和模型不随仓库提交，按项目 README 分阶段安装；
- 课程来源和许可说明见 [LICENSE.md](LICENSE.md)。

## 学习时间线

| 时间 | 产出 |
| --- | --- |
| 2026-07 | LangChain 基础、RAG 数据流和手写 ReAct Demo |
| 2026-08 | LangGraph 搜索 Workflow、自建 Agent 框架、Memory 与 RAG 代码改编 |
| 2026-09 | 上下文工程与代码库维护助手学习改编 |
| 后续 | 围绕实际项目补充 FastAPI、MySQL、Docker、评测和可观测性 |

课程来源：[Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents)。
