# AI 应用工程学习与项目展示

这是一个面向 AI 应用工程岗位的学习与项目仓库，记录 Agent、RAG、工作流、工具调用和相关工程化实践。仓库内容以可追溯的代码改编、技术验证和后续独立项目为主。

## 技术方向

- Python 大模型应用开发
- ReAct Agent 与工具调用
- LangChain / LangGraph
- RAG、Embedding、向量检索和知识库
- Memory、Context 和 Agent Harness
- FastAPI、MySQL、Docker、评测与可观测性

## 当前项目与实践

### Hello Agents 学习改编

目录：[hello_agent_study](hello_agent_study/)

| 时间 | 项目 | 技术内容 |
| --- | --- | --- |
| 2026-07 | ReAct 旅行助手 | Thought-Action-Observation、工具注册、Action 解析和循环边界 |
| 2026-08 | LangGraph 搜索 Workflow | State、Node、Edge、条件流程和检查点 |
| 2026-08 | 自建 Agent 框架 | Agent 抽象、Simple/ReAct/Reflection/Plan-and-Solve、工具系统 |
| 2026-08 | Memory 与 RAG | 记忆类型、生命周期、文档摄取、检索增强和综合问答 |

这些内容来源于 Datawhale `Hello-Agents`，已根据本地学习环境进行配置适配和脱敏，具体改动记录在各项目目录 README 中。

## 代码与工程规范

- 使用 `.env.example` 提供配置模板，真实密钥只保存在本地；
- 不提交个人绝对路径、数据库密码、模型文件和运行缓存；
- 大型模型、数据库服务和重型依赖按项目需要单独准备；
- README 记录项目目标、技术栈、架构、运行方式、改动范围和当前边界；
- 教程改编与独立项目分开标注，避免混淆学习练习和原创项目。

## 学习时间线

| 时间 | 阶段性内容 |
| --- | --- |
| 2026-07 | LangChain 基础、Prompt、Chain、结构化输出、RAG 和工具调用 |
| 2026-07 | 手写 ReAct Agent 与 Agent 基础概念 |
| 2026-08 | LangGraph Workflow 和 HelloAgents 自建框架 |
| 2026-08 | Memory、RAG、Embedding、MQE/HyDE 和文档问答系统 |
| 后续 | 面向真实项目补充接口封装、数据库、部署、评测和可观测性 |

## 仓库结构

```text
hello_agent_study/
├── chapter01_react_travel_agent/
├── chapter06_langgraph_search/
├── chapter07_helloagents_framework/
└── chapter08_memory_and_rag/
projects/
docs/
```

## 课程来源

- [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents)
- [Hello Agents 在线教程](https://hello-agents.datawhale.cc/)

本仓库用于学习记录和项目展示。课程改编内容会保留来源、改动说明和边界，后续独立项目将单独说明业务目标、工程设计和个人实现内容。
