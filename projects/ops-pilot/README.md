# OpsPilot：多智能体 AIOps 诊断工作台

这是一个面向 OnCall / SRE 场景的多智能体故障诊断项目，接收用户故障描述或 Alertmanager 告警，通过 Skill 路由、RAG 检索和 MCP 工具收集证据，最后生成带引用和审计信息的 Markdown 诊断报告。

本目录是对开源项目的学习整理与二次开发版本，重点用于理解 Agent、LangGraph、RAG、工具调用、权限边界和后台任务工程。它适合学习和面试展示，不应直接当作生产系统使用。

## 我在本项目中完成的工作

- 保留并梳理原项目的 fast / deep 双诊断图、Skill 路由、工具执行、证据聚合和报告生成架构。
- 增加 `app/lite/` 单机学习路径，将 `route → retrieve → collect_evidence → synthesize → finalize` 的核心 Agent 流程拆开验证。
- 使用本地 FAISS 与 Ollama Embedding 完成轻量检索适配，并加入透明的关键词候选预筛，控制首次本地索引规模。
- 为模型或检索不可用的情况保留确定性报告降级路径，明确展示依赖缺失和证据边界。
- 补充架构、Lite Mode、评测、并发和简历事实说明，区分继承代码、个人改动和已验证范围。
- 将本地绝对路径改为通用命令或运行时路径，移除公开版本中的 `.env`、个人环境记录和生成报告。

## 核心架构

```text
用户 / Alertmanager
        ↓
FastAPI 接入与参数校验
        ├── 即时 SSE 诊断
        └── PostgreSQL 任务事实 → Redis Streams → Worker
                                      ↓
                             DiagnosisRunner
                         ┌────────────┴────────────┐
                         ▼                         ▼
                 fast：计划执行重规划       deep：专业 Agent 取证
                         └────────────┬────────────┘
                                      ↓
                    Skill / RAG / MCP / 本地工具 / LLM
                                      ↓
                          Evidence、RCA 与诊断报告
```

完整架构使用 FastAPI、LangGraph、Milvus、Redis、PostgreSQL、MCP 和 Docker。Lite Mode 使用 LangGraph、FAISS、可选 Ollama 和确定性降级逻辑，便于在没有完整基础设施时理解数据流。

## 目录说明

| 路径 | 作用 |
| --- | --- |
| `app/agents/` | fast 图节点和 deep 专业 Agent |
| `app/orchestration/` | 诊断模式选择、执行、审计和事件转换 |
| `app/runtime/` | Agent Harness、权限、审批、工具运行和预算 |
| `app/rag/`、`app/core/` | 切分、向量检索、混合召回、重排和模型适配 |
| `app/lite/` | 单机 Lite Mode 入口、检索和只读证据采集 |
| `app/skills/` | Skill 模型、注册和 Playbook |
| `mcp_servers/` | 系统、网络、Windows 日志和 Docker 工具服务 |
| `benchmark/` | 检索 / RAG 评测脚本与小型评测集 |
| `data/kb_corpus/` | Lite Mode 使用的上游公开语料目录；当前公开副本不提交大批量语料 |
| `frontend/` | 静态 Web UI |
| `open-webSearch-main/` | 第三方本地联网搜索服务 |
| `docs/` | 架构、Lite Mode、评测和运行边界说明 |

## 配置与运行

公开仓库只提供配置模板。运行前复制 `.env.example` 或 `lite.env.example` 为本地 `.env`，再填写自己的模型、Embedding 和服务配置；真实 Key 只保存在本机，不能提交到 Git。

完整服务需要 Docker Compose、Python 3.12、Milvus、Redis、PostgreSQL、Embedding 服务和模型 Provider。基础设施与后台 Worker 的启动方式见 `docker-compose.yml` 和 [系统架构说明](docs/ARCHITECTURE.md)。

Lite Mode 可以先做不依赖外部服务的状态流检查：

```bash
python -m app.lite.cli "我电脑最近很卡" --skip-rag
```

准备少量本地语料到 `data/kb_corpus/` 并配置本地 Embedding 后，可以运行轻量检索：

```bash
python -m app.lite.cli "主机内存压力和 OOM 怎么排查" --max-docs 20
```

本次整理没有安装依赖、下载模型、启动 Docker 或调用外部模型。公开副本按仓库规则排除了大批量数据集；如需完整 RAG 演示，可根据 `scripts/fetch_kb_corpus.ps1` 获取上游公开语料。完整运行可能产生模型调用费用和外部数据传输，需先确认服务、凭据和数据范围。

## 验证边界

已经记录并保留的验证范围包括 Lite Mode 状态流、有限本地检索和一次模型报告生成。完整 FastAPI、Milvus、Redis、PostgreSQL、MCP、Worker 和 deep 图没有在本次同步中重新验证，不能把它们描述成当前环境已经完成端到端部署。

更多说明：

- [系统架构与已知限制](docs/ARCHITECTURE.md)
- [Lite Mode](docs/LITE_MODE.md)
- [检索与 RAG 评测](benchmark/README.md)
- [并发与队列测试指南](docs/CONCURRENCY_TEST_GUIDE.md)
- [简历事实边界](docs/RESUME_TRUTH.md)
- [Redis OnCall SOP](docs/sop/redis_oncall_sop.md)
- [MySQL OnCall SOP](docs/sop/mysql_oncall_sop.md)

## 来源与许可证

本项目的原始代码来源于 [Kkkirito-123/mutil-rag-agent](https://github.com/Kkkirito-123/mutil-rag-agent)，原项目代码使用 MIT License。本目录保留原项目许可证和第三方来源说明。

- `open-webSearch-main/` 来源于 [Aas-ee/open-webSearch](https://github.com/Aas-ee/open-webSearch)，使用 Apache License 2.0。
- `data/kb_corpus/awesome-prometheus-alerts/` 的上游来源是 [samber/awesome-prometheus-alerts](https://github.com/samber/awesome-prometheus-alerts)，原始项目标注为 CC BY 4.0；当前公开副本不包含这批大批量语料。
- 其他第三方资料以各自目录中的许可证和上游说明为准。
