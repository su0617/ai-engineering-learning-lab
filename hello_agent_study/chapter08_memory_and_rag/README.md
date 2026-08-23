# 第八章：记忆与检索

> 学习改编时间：2026-08-23

本目录整理 Datawhale `Hello-Agents` 第八章的代码改编，主题覆盖 Memory、RAG、工具集成和综合文档问答助手。

## 项目内容

| 示例 | 技术主题 |
| --- | --- |
| `01`-`03` | MemoryTool 基础操作、分层架构、工作记忆和生命周期 |
| `04`-`05` | MarkItDown 文档处理、分块、MQE、HyDE 和高级检索 |
| `06`-`09` | 记忆整合、RAG 问答、Agent 工具集成、四类记忆对比 |
| `10` | 完整 RAG 数据处理和问答管道 |
| `11` | Memory + RAG + Gradio 的综合文档问答助手 |

## 技术栈

- Python 3.10+
- HelloAgents 0.2.9
- MemoryTool / RAGTool
- Qdrant 向量数据库
- Neo4j 图数据库
- MarkItDown 文档转换
- Embedding、MQE、HyDE
- Gradio Web UI
- DeepSeek/OpenAI 兼容 API

## 核心架构

```text
文档或对话输入
       ↓
统一处理与结构化
       ↓
MemoryTool / RAGTool
       ├── 工作记忆、情景记忆、语义记忆、感知记忆
       ├── 文本分块与 Embedding
       ├── Qdrant 向量检索
       └── 可选 Neo4j 关系存储
       ↓
Agent 或问答助手
       ↓
回答、记忆更新和统计报告
```

## 本次改编

- 保留课程的 11 个循序渐进示例，便于按教材对照阅读。
- 统一使用 `LLM_MODEL_ID`、`LLM_API_KEY` 和 `LLM_BASE_URL` 配置聊天模型，可接 DeepSeek 或其他 OpenAI 兼容服务。
- 将真实配置改为 `.env.example` 占位模板，没有提交 API Key、个人路径或本地运行数据。
- 增加分层依赖文件：`requirements-core.txt` 用于轻量接口环境，`requirements-complete.txt` 仅供以后完整运行时参考。
- 增加 `check_syntax.py`，在没有完整数据库和模型环境时进行标准库语法检查。
- 第 11 个 Gradio 示例默认监听 `127.0.0.1`，生成报告统一放入被忽略的 `outputs/` 目录。

## 配置说明

```powershell
conda activate agent_study_env
Copy-Item .env.example .env
```

然后填写自己的模型配置，例如：

```dotenv
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=你的APIKey
LLM_BASE_URL=https://api.deepseek.com
```

如果使用中转站，只需要把 `LLM_BASE_URL` 改成中转站提供的 OpenAI 兼容地址。真实 Key 只保存在本机 `.env` 中。

## 当前验证方式

本次只进行轻量验证，不安装完整依赖、不下载模型、不启动 Qdrant 或 Neo4j：

```powershell
conda activate agent_study_env
python check_syntax.py
```

完整运行第八章需要额外安装 `requirements-complete.txt`，并配置 Embedding、Qdrant、Neo4j 等服务。由于依赖和资源开销较大，暂不作为当前学习阶段的必做步骤。

## 项目定位

这是课程代码的学习改编和架构阅读记录，不是独立生产项目。它的主要价值是理解：

- 记忆为什么要按类型和生命周期管理；
- RAG 如何从文档摄取走到检索生成；
- MemoryTool 和 RAGTool 如何作为 Agent 工具被组合；
- 向量检索、知识图谱和大模型在系统中的职责边界。

课程来源：[Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents)。
