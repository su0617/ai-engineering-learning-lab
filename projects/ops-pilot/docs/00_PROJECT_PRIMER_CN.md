# OpsPilot 项目预习手册

> 用途：概念扫盲、技术栈预习、全项目导览。
>
> 这不是背诵资料。第一遍只需要形成印象：这个系统有哪些层、每层解决什么问题、一次请求如何流动。后续源码课会反复回到这些概念。

## 0. 先知道这个项目到底是什么

OpsPilot 是一个面向 OnCall / SRE 场景的多 Agent AIOps 故障诊断系统。

一句话概括：

> 用户输入故障描述或系统收到告警后，系统选择诊断模式和 Skill，使用 RAG 与工具收集证据，再由 Agent 生成可追溯的诊断报告。

它不是单纯的聊天机器人。它同时包含：

- Web 后端：FastAPI、HTTP、SSE。
- Agent 编排：LangGraph、State、Node、Edge、Loop。
- 多 Agent：日志、指标、基础设施、Runbook 等专业 Agent。
- RAG：Embedding、Milvus、BM25、RRF、Rerank。
- 工具系统：本地工具、MCP、权限控制、审批。
- 异步任务：Redis Streams、Worker、重试和死信队列。
- 事实审计：PostgreSQL 保存任务、证据、工具调用和报告。
- 部署：Docker、Docker Compose、MinIO、etcd。
- 评测：检索评测、RAG 评测、并发压测。

完整项目和 Lite Mode 的关系：

| 路径 | 用途 | 主要组件 |
|---|---|---|
| 完整项目 | 理解生产形态和完整架构 | FastAPI、Milvus、Redis、PostgreSQL、MCP、Worker、fast/deep 图 |
| Lite Mode | 本机快速验证核心流程 | LangGraph、FAISS、Ollama bge-m3、DeepSeek |

Lite Mode 不是要代替完整项目，而是让核心链路在个人电脑上低成本运行。

---

## 1. 场景名词扫盲

### 1.1 AIOps

- 全称：Artificial Intelligence for IT Operations。
- 中文：面向 IT 运维的人工智能，简称智能运维。
- 读法：A-I-Ops，常读作“诶艾奥普斯”。
- 本项目作用：用 Agent、RAG 和工具辅助排查主机、网络、容器、Redis、MySQL 等故障。

### 1.2 OnCall

- 中文：值班响应、故障值班。
- 读法：“昂 call”。
- 含义：线上系统发生告警后，由值班工程师响应和排查。

### 1.3 SRE

- 全称：Site Reliability Engineering。
- 中文：站点可靠性工程。
- 读法：S-R-E。
- 含义：通过软件工程方法提高系统可靠性、可用性和可观测性。

### 1.4 Alert / Alertmanager

- Alert：告警，读作“额勒特”。
- Alertmanager：告警管理器，读作“额勒特 manager”。
- 本项目作用：外部监控系统可以通过 Webhook 把告警发送给项目。

### 1.5 Incident

- 中文：故障事件。
- 读法：“因西登特”。
- 含义：一次可能影响服务的异常事件，通常包含严重级别、服务、时间、告警和处理状态。

### 1.6 RCA

- 全称：Root Cause Analysis。
- 中文：根因分析。
- 读法：R-C-A。
- 含义：不只描述“哪里坏了”，还要分析“为什么坏”。

### 1.7 Runbook 与 Playbook

- Runbook：运行手册、排障手册，读作“润布克”。
- Playbook：执行剧本，读作“普雷布克”。
- 区别：Runbook 更像通用操作文档；Playbook 更强调针对某类任务应该按什么策略和顺序执行。

### 1.8 Skill

- 中文：技能。
- 读法：“斯给欧”。
- 本项目含义：一个故障领域的名称、用途、Playbook 和允许工具的组合。
- 已有示例：主机资源诊断、网络诊断、容器诊断、通用 OnCall。

---

## 2. Agent 核心概念

### 2.1 LLM

- 全称：Large Language Model。
- 中文：大语言模型。
- 读法：L-L-M。
- 本项目示例：DeepSeek。
- 职责：理解问题、规划步骤、选择工具、判断结果、生成报告。

LLM 不是整个 Agent。Agent 是“LLM + 状态 + 工具 + 循环 + 终止条件 + 工程控制”。

### 2.2 Agent

- 中文：智能体。
- 读法：“诶真特”。
- 简化定义：能够根据当前状态决定下一步，并可以调用工具完成任务的程序。

普通问答：

```text
用户问题 → LLM → 回答
```

Agent：

```text
用户问题
→ 判断任务
→ 制定计划
→ 调用工具
→ 读取结果
→ 调整计划
→ 判断是否完成
→ 输出答案
```

### 2.3 Agent Loop

- 中文：Agent 循环。
- 读法：“Agent 路普”。
- 含义：模型在“推理—调用工具—读取结果—继续推理”之间循环，直到任务完成或触发终止条件。

为什么需要 Loop：复杂任务通常无法通过一次模型调用完成。

主要风险：

- 死循环。
- 重复调用相同工具。
- 任务没有真正推进。
- Token 和费用不断增加。
- 工具失败后仍盲目重试。

### 2.4 Plan-Execute-Replan

- Plan：规划，读作“普兰”。
- Execute：执行，读作“艾克西Q特”。
- Replan：重新规划，读作“瑞普兰”。

流程：

```text
Planner 生成计划
→ Executor 执行当前步骤
→ Replanner 检查结果
→ 继续、换 Skill、重新规划或结束
```

### 2.5 State

- 中文：状态。
- 读法：“斯得特”。
- 含义：Agent 当前拥有的数据，例如输入、计划、历史步骤、证据、最终回答。

State 可以理解为 Agent 工作时共同填写的一张任务表。

### 2.6 Node / Edge / Graph

- Node：节点，读作“诺德”，代表一个处理步骤。
- Edge：边，读作“艾居”，代表节点之间的跳转。
- Graph：图，读作“格拉夫”，代表完整流程。
- Conditional Edge：条件边，根据 State 决定下一节点。

### 2.7 Tool Call

- Tool：工具，读作“图欧”。
- Tool Call：工具调用。
- 含义：模型选择一个工具并生成参数，由程序校验并执行，再把结果放回 Agent 上下文。

完整流程：

```text
模型选择工具
→ 生成参数
→ 参数校验
→ 权限检查
→ 工具执行
→ 超时/异常处理
→ Tool Result 回填
→ 模型继续判断
```

### 2.8 Function Calling

- 中文：函数调用。
- 读法：“Function Calling”。
- 含义：把工具名称和参数结构告诉模型，让模型输出结构化的调用请求。
- 注意：模型只是提出调用，不应该由模型直接执行系统命令。

### 2.9 Harness

- 中文可理解为：Agent 运行框架、运行控制外壳。
- 读法：“哈尼斯”。
- 本项目位置：`app/runtime/agent_harness.py`。
- 负责：Prompt 模板、循环限制、Token 预算、工具策略、错误分类、降级和运行统计。

业务 Agent 负责“做什么”，Harness 负责“怎么安全、稳定、有预算地运行”。

### 2.10 Guardrail

- 中文：安全护栏。
- 读法：“嘎德瑞尔”。
- 作用：限制危险工具、危险参数、写操作和未经授权的副作用。

### 2.11 Evidence

- 中文：证据。
- 读法：“艾维登斯”。
- 本项目含义：由日志、指标、RAG、工具或历史事件产生的可引用事实。
- 价值：让诊断结论可以追溯，减少 LLM 脱离事实自由发挥。

### 2.12 Session、Context、Memory、RAG

四者容易混淆：

| 概念 | 中文 | 解决的问题 |
|---|---|---|
| Session | 会话 | 哪些请求属于同一次交互 |
| Context | 当前上下文 | 本次模型调用应该看到什么 |
| Memory | 记忆 | 跨步骤或跨会话保存什么 |
| RAG | 外部知识检索 | 从知识库中找什么事实 |

简化例子：

- Session：你和系统这次排查 Redis 故障的会话编号。
- Context：本轮发给模型的告警、历史步骤和工具结果。
- Memory：上一次排查同一服务时保存的经验。
- RAG：从 Redis OnCall 手册里检索到的排障步骤。

### 2.13 Prompt

- 中文：提示词。
- 读法：“普rompt”。
- System Prompt：定义角色、规则和边界。
- User Prompt：用户本次请求。
- Tool Result：工具执行结果，也会进入后续上下文。

### 2.14 Token

- 中文常称：词元。
- 读法：“偷肯”。
- 含义：模型处理文本时使用的基本计量单位。
- 风险：Context 越长，Token、延迟和费用通常越高。

### 2.15 Retry、Fallback、Timeout、Idempotency

- Retry：重试，读作“瑞踹”。
- Fallback：降级/兜底，读作“佛拜克”。
- Timeout：超时，读作“太姆奥特”。
- Idempotency：幂等性，读作“艾登泼腾西”。

幂等性的意思：同一个任务重复执行，不应该产生重复副作用。

错误不能全部重试：

- 网络抖动、连接重置：可能适合重试。
- 参数格式错误：重试相同参数没有意义，应让模型重新规划。
- 权限拒绝：不能靠重试绕过。
- 非幂等写操作：重试前必须防止重复执行。

---

## 3. Web 后端概念

### 3.1 HTTP 与 API

- HTTP：HyperText Transfer Protocol，超文本传输协议，读作 H-T-T-P。
- API：Application Programming Interface，应用程序编程接口，读作 A-P-I。

浏览器或客户端通过 HTTP 请求 API。

常见方法：

- GET：读取数据。
- POST：提交数据或创建任务。
- PUT/PATCH：更新数据。
- DELETE：删除数据。

### 3.2 FastAPI

- Python Web 框架。
- 读法：Fast A-P-I。
- 本项目作用：提供诊断、健康检查、队列、Skill、文档、评测等接口。

FastAPI 不是 Agent，它是 Agent 系统的 HTTP 入口。

### 3.3 Route / Router

- Route：路由，读作“入特”。
- Router：路由器。
- 含义：把 URL 和处理函数对应起来。

例如：

```text
POST /api/v1/aiops/diagnose
→ aiops_diagnose()
```

### 3.4 Pydantic

- Python 数据校验库。
- 读法：“派丹提克”。
- 作用：检查请求字段类型、长度、默认值，并把字典转换成结构化对象。

### 3.5 JSON

- 全称：JavaScript Object Notation。
- 中文：一种常用数据交换格式。
- 读法：“杰森”。

### 3.6 Uvicorn

- Python ASGI Server。
- 读法：“尤维康”。
- 作用：真正监听端口并运行 FastAPI 应用。

### 3.7 ASGI

- 全称：Asynchronous Server Gateway Interface。
- 中文：异步服务器网关接口。
- 读法：A-S-G-I。
- 作用：让 Python Web 应用支持异步请求、长连接和流式响应。

### 3.8 async / await

- async：声明异步函数。
- await：等待一个异步操作完成，同时允许事件循环处理其他任务。

适合：网络请求、数据库访问、模型调用、工具调用等等待时间较长的操作。

### 3.9 SSE

- 全称：Server-Sent Events。
- 中文：服务端发送事件。
- 读法：S-S-E。
- 作用：服务器可以持续把 Agent 的阶段结果推送给浏览器。

项目中的事件示例：

```text
start
plan
step_complete
replan
tool_call
report
complete
error
```

### 3.10 Middleware 与 Lifespan

- Middleware：中间件，读作“米德尔威尔”。在请求进入业务代码前后统一执行日志、跨域、限流等逻辑。
- Lifespan：应用生命周期。启动时连接数据库，关闭时释放资源。

---

## 4. RAG 概念

### 4.1 RAG

- 全称：Retrieval-Augmented Generation。
- 中文：检索增强生成。
- 读法：常读“拉格”。

流程：

```text
文档准备
→ 文档切分
→ Embedding
→ 写入向量库
→ 用户查询向量化
→ 检索 Top-K
→ 可选融合和重排
→ 拼入 Prompt
→ LLM 生成答案
```

### 4.2 Chunk

- 中文：文本块。
- 读法：“常克”。
- 含义：长文档切成的小段。
- 太大：包含太多无关内容。
- 太小：上下文可能被切断。

### 4.3 Parent-Child Chunk

- Parent：较大的父文本块。
- Child：较小的子文本块。
- 思路：用小块提高检索精度，命中后返回更完整的父块保证上下文。

### 4.4 Embedding

- 中文：嵌入向量。
- 读法：“恩贝丁”。
- 作用：把文本转换成一组数字，使语义相近的文本在向量空间中更接近。
- 本项目默认：Ollama + bge-m3。

### 4.5 Vector / Vector Database

- Vector：向量，读作“维克特”。
- Vector Database：向量数据库。
- 用途：按向量相似度寻找语义相关文档。

### 4.6 FAISS 与 Milvus

- FAISS：Facebook AI Similarity Search，读作“费斯”。适合本地、进程内快速向量检索。
- Milvus：向量数据库，读作“米尔沃斯”。适合服务化、持久化、更大规模数据和多人/多进程访问。

Lite Mode 使用 FAISS，完整项目使用 Milvus。

### 4.7 BM25

- 读法：B-M-25。
- 含义：经典关键词检索算法，关注词频、文档长度和关键词区分度。
- 优点：故障码、命令、错误文本等精确关键词检索效果好。

### 4.8 Hybrid Search

- 中文：混合检索。
- 读法：“Hybrid Search”。
- 含义：同时使用向量语义检索和 BM25 关键词检索。

### 4.9 RRF

- 全称：Reciprocal Rank Fusion。
- 中文：倒数排名融合。
- 读法：R-R-F。
- 作用：把多个检索器的排名结果融合成一个统一排名。

### 4.10 Rerank

- 中文：重排序。
- 读法：“瑞 rank”。
- 作用：使用更精确但成本更高的模型，对初步召回结果重新排序。

### 4.11 Top-K

- 含义：返回相关度最高的 K 条结果。
- K 太小：可能漏掉关键证据。
- K 太大：增加噪声、Context 和费用。

### 4.12 Recall、Precision、Faithfulness

- Recall：召回率，应该找到的相关内容找到了多少。
- Precision：精确率，找到的内容里有多少真的相关。
- Faithfulness：忠实度，答案是否由给定证据支持。

---

## 5. 数据、队列和部署概念

### 5.1 Redis

- 内存数据服务。
- 读法：“瑞迪斯”。
- 本项目用途：Streams 队列、短期状态、限流和并发槽。

### 5.2 Redis Streams

- Streams：消息流。
- Producer：生产者，把任务写入 Stream。
- Consumer：消费者，从 Stream 读取任务。
- Consumer Group：消费者组，让多个 Worker 分工处理任务。
- ACK：Acknowledgement，确认消息已经成功处理。
- DLQ：Dead Letter Queue，死信队列，保存多次失败后无法继续处理的任务。

### 5.3 Worker

- 中文：后台工作进程。
- 读法：“沃克”。
- 作用：从 Redis Stream 取出任务，运行 Agent，再把结果写入 PostgreSQL。

### 5.4 PostgreSQL

- 关系型数据库。
- 读法：“Postgres”常读作“坡斯特格瑞斯”。
- 本项目用途：保存任务、Incident、Evidence、AgentRun、ToolCall、Approval 和 Report 等事实。

常见词：

- Table：表。
- Row：行。
- Column：列。
- Primary Key：主键。
- Foreign Key：外键。
- Index：索引。
- Transaction：事务。
- Connection Pool：连接池。

### 5.5 Docker

- 容器技术。
- 读法：“刀克”。
- Image：镜像，是容器模板。
- Container：容器，是镜像的运行实例。
- Dockerfile：描述如何构建镜像。
- Docker Compose：用 YAML 文件编排多个服务。
- Volume：持久化数据卷。
- Network：容器之间通信的网络。

### 5.6 etcd

- 分布式键值存储。
- 读法：“et-see-dee”或直接读字母。
- 本项目作用：Milvus 的元数据依赖之一。

### 5.7 MinIO

- 对象存储服务。
- 读法：“迷你-O”。
- 本项目作用：Milvus 用它保存对象数据。

### 5.8 MCP

- 全称：Model Context Protocol。
- 中文：模型上下文协议。
- 读法：M-C-P。
- 作用：用统一协议向 Agent 暴露工具和外部资源。

本项目有系统、联网搜索、Windows 日志、网络和 Docker 等 MCP 服务。

---

## 6. 项目完整架构图

```text
用户 / Alertmanager
        │
        ▼
FastAPI API
        │
        ├──────── 同步诊断 ────────┐
        │                           │
        │                           ▼
        │                    DiagnosisRunner
        │                           │
        │                           ├── fast graph
        │                           └── deep graph
        │
        └──────── 异步诊断 ──────────────┐
                                        │
                                  PostgreSQL 建任务
                                        │
                                  Redis Stream 入队
                                        │
                                      Worker
                                        │
                                  DiagnosisRunner

DiagnosisRunner
        │
        ├── Skill / Playbook
        ├── RAG / Milvus / BM25 / RRF / Rerank
        ├── MCP / local tools
        ├── Evidence
        ├── Harness / permissions / budget
        └── Report / Wiki / audit
```

### 6.1 同步链路

```text
POST /api/v1/aiops/diagnose
→ aiops_diagnose()
→ aiops_service.stream_diagnose()
→ run_diagnosis_graph()
→ fast/deep LangGraph
→ SSE 持续返回事件
```

适合：用户在页面上即时查看诊断过程。

### 6.2 异步链路

```text
POST /api/v1/aiops/diagnose/submit
→ PostgreSQL 创建任务
→ Redis Stream 入队
→ 立即返回 task_id
→ Worker 消费
→ 执行 DiagnosisRunner
→ 保存 Evidence 和 Report
```

适合：耗时任务、高并发、后台执行和失败重试。

---

## 7. fast 和 deep 两套 Agent 图

### 7.1 fast 模式

```text
START
  ↓
SkillRouter
  ↓
Planner
  ↓
Executor
  ↓
Replanner
  ├── 继续 Executor
  ├── 换 Skill 后重新 Planner
  └── END
```

特点：

- 路径短。
- 适合较明确的单类故障。
- 使用 Plan-Execute-Replan 循环。
- 工具结果会影响后续计划。

### 7.2 deep 模式

```text
IncidentManager
  ↓
CorrelationContext
  ↓
EvidencePlan
  ├── LogAgent
  ├── MetricAgent
  ├── InfraAgent
  └── RunbookAgent
          ↓
   EvidenceReducer
          ↓
       RCAJudge
          ↓
 RemediationPlanner
          ↓
        Report
```

特点：

- 多个专业 Agent 按证据类型分工。
- 中间推理隔离，只向公共 State 写压缩后的 Evidence。
- 统一归并、评分、根因判断和修复规划。
- 更适合复杂事件和交叉取证。

### 7.3 为什么不让一个 Agent 全做

- Context 容易膨胀。
- 职责混乱。
- 某类工具失败可能拖垮全部流程。
- 证据来源难以追踪。
- 并行能力差。

---

## 8. 源码地图

### 8.1 服务入口

- `app/main.py:43`：FastAPI 生命周期，连接和关闭外部资源。
- `app/main.py:86`：创建 FastAPI 应用。
- `app/main.py:153`：注册 API 路由。

### 8.2 AIOps 接口

- `app/api/v1/aiops.py:37`：异步提交诊断任务。
- `app/api/v1/aiops.py:133`：同步 SSE 诊断接口。

### 8.3 统一运行器

- `app/orchestration/diagnosis_runner.py:80`：解析 fast/deep 有效模式。
- `app/orchestration/diagnosis_runner.py:100`：统一运行诊断图并生成运行时事件。

### 8.4 fast 图

- `app/agents/graph.py:56`：Replanner 后的结束/继续/重规划判断。
- `app/agents/graph.py:95`：构建 fast LangGraph。
- `app/agents/state.py:34`：fast 图 State。
- `app/agents/skill_router.py`：选择 Skill。
- `app/agents/planner.py`：制定计划。
- `app/agents/executor.py`：执行当前步骤和工具。
- `app/agents/replanner.py`：判断继续、换 Skill 或结束。

### 8.5 deep 图

- `app/diagnosis_graphs/deep_diagnosis_graph.py:60`：专业 Agent 列表。
- `app/diagnosis_graphs/deep_diagnosis_graph.py:898`：构建 deep LangGraph。
- `app/agents/state_deep.py:25`：deep 图 State。
- `app/agents/log_agent.py`：日志证据。
- `app/agents/metric_agent.py`：指标证据。
- `app/agents/infra_agent.py`：基础设施证据。
- `app/agents/runbook_agent.py`：Runbook 证据。

### 8.6 Harness 与工具安全

- `app/runtime/agent_harness.py`：Prompt、预算、错误分类和降级策略。
- `app/runtime/tool_runner.py`：工具执行。
- `app/runtime/tool_filter.py`：工具筛选。
- `app/runtime/permissions.py`：权限模式。
- `app/runtime/approvals.py`：人工审批。
- `app/runtime/transitions.py`：状态迁移记录。

### 8.7 RAG

- `app/core/splitter.py`：文档切分。
- `app/core/embedding.py`：Embedding。
- `app/core/milvus.py`：Milvus 连接管理。
- `app/core/hybrid_retriever.py`：混合检索。
- `app/core/reranker.py`：重排序。
- `app/rag/retrieval.py`：构建 RAG 上下文。
- `scripts/ingest_kb_corpus.py`：把文档导入 Milvus。

### 8.8 Redis、PostgreSQL 和 Worker

- `app/queue/redis_streams.py`：Redis Stream 队列。
- `app/diagnosis_worker.py`：消费诊断任务。
- `app/db/postgres.py`：PostgreSQL 连接和表结构。
- `app/incidents/`：事件和任务事实。
- `app/evidence/`：Evidence 模型和存储。

### 8.9 Skill 与 MCP

- `app/skills/registry.py`：Skill 注册表。
- `app/skills/loader.py`：加载 Skill 定义。
- `app/skills/definitions/*/SKILL.md`：各领域 Playbook。
- `app/core/mcp_client.py`：MCP 客户端。
- `mcp_servers/`：各工具服务。

### 8.10 部署和评测

- `Dockerfile`：构建 API/Worker 共用镜像。
- `docker-compose.yml`：编排完整服务。
- `benchmark/`：检索与 RAG 评测。
- `scripts/loadtest.py`：并发测试。
- `scripts/mock_alert.py`：模拟告警。

---

## 9. 关键数据对象

### 9.1 DiagnosisRequest

用户请求模型，通常包含：

- query：故障描述。
- session_id：会话标识。
- diagnosis_mode：fast 或 deep。

### 9.2 PlanExecuteState

fast 图状态，核心概念包括：

- input：原始问题。
- selected_skill：选中的 Skill。
- plan：未执行计划。
- past_steps：已执行步骤和结果。
- response：最终回答。
- pending_reroute：是否需要切换 Skill 并重新规划。
- transition_history：状态迁移历史。

### 9.3 DeepDiagnosisState

deep 图状态，核心概念包括：

- incident：当前事件。
- correlation_context：关联事件和历史经验。
- evidence_plan：准备派遣哪些专业 Agent。
- evidences：并行累加的证据。
- root_cause_candidates：候选根因。
- rca：根因判断。
- remediation：修复计划。
- response：最终报告。

### 9.4 Evidence

Evidence 至少需要说明：

- 来源是什么。
- 类型是什么。
- 内容是什么。
- 置信度如何。
- 是否失败或降级。
- 最终结论引用了哪条证据。

### 9.5 RuntimeEvent

Agent 内部执行状态被转换成统一事件，例如：

```text
start
mode_selected
transition
plan
step_complete
tool_call
report
complete
error
```

API 可以把这些事件通过 SSE 发给前端，Worker 也可以用相同事件做日志和审计。

---

## 10. 技术之间如何联动

### 10.1 FastAPI、LangGraph、LLM 的关系

```text
FastAPI：接收请求
LangGraph：决定步骤和流程
LLM：在某些节点中理解、规划和生成
```

### 10.2 RAG 与 Tool 的区别

```text
RAG：从知识库找已有知识
Tool：从实时系统获取信息或执行动作
```

例如：

- RAG 找到“Redis 内存过高的排查手册”。
- Tool 获取“当前 Redis 内存使用率”。

### 10.3 Redis、PostgreSQL、Milvus 的区别

```text
Redis：队列、缓存、短期状态、并发控制
PostgreSQL：结构化事实、任务状态、审计记录
Milvus：向量和语义检索
```

### 10.4 API 和 Worker 的区别

```text
API：快速接收和响应请求
Worker：后台执行耗时任务
```

### 10.5 Skill、Agent、Tool 的区别

```text
Skill：某类任务的知识、策略和工具边界
Agent：根据状态做决策并推进任务
Tool：完成一个具体能力的执行单元
```

---

## 11. 从开发者角度看系统

不要只问“用了什么技术”，还要问以下问题。

### 11.1 边界

- 哪层负责 HTTP？
- 哪层负责业务编排？
- 哪层负责 Agent 图？
- 哪层负责工具安全？
- 哪层负责持久化？

### 11.2 输入输出

- 一个函数接收什么？
- 返回什么？
- 返回的是最终值、事件流还是 State patch？

### 11.3 失败处理

- LLM 超时是否重试？
- Tool 参数错误是否应该重试？
- Redis 不可用是否允许同步模式继续？
- Milvus 不可用是否降级到无 RAG？
- Worker 重复收到任务如何保证幂等？

### 11.4 状态和副作用

- 哪些操作只是读？
- 哪些操作会写数据库？
- 哪些工具可能重启容器或修改系统？
- 重试是否会造成重复副作用？

### 11.5 扩展性

- 新增 Skill 改哪些文件？
- 新增专业 Agent 改哪些图和 State？
- 新增 MCP 工具怎么注册？
- 新增诊断模式如何接入 Runner？

---

## 12. 高频面试预览

### 12.1 为什么 Agent 需要 Loop？

因为复杂任务需要多次获取外部信息，并根据工具结果动态调整后续步骤。一次模型调用无法保证拿到所有实时证据。

### 12.2 如何避免 Agent 死循环？

- 限制最大图递归次数和工具轮数。
- 检查计划是否为空。
- 识别重复工具和重复参数。
- 检查状态是否真正推进。
- 超过 Token、时间或费用预算时终止或降级。

最大轮数只是最后兜底，不等于真正判断“任务是否有进展”。

### 12.3 Tool 失败后怎么办？

先分类：

- 暂时性网络错误可以有限重试。
- 参数校验错误应回填给模型重新规划。
- 权限错误直接阻断并说明原因。
- 高风险写操作不能自动重复。
- 全部失败时产生带错误元数据的 Evidence，而不是伪造结果。

### 12.4 Memory、Session、Context、RAG 有什么区别？

Session 标识会话；Context 是本轮输入模型的内容；Memory 保存跨步骤/跨会话信息；RAG 从外部知识库检索事实。

### 12.5 为什么使用 Redis Streams？

把请求接入和耗时诊断解耦。API 快速返回 task_id，Worker 后台消费任务；同时支持消费者组、ACK、重试和死信处理。

### 12.6 为什么同时需要 PostgreSQL 和 Redis？

Redis 负责快速消息传递和临时状态；PostgreSQL 负责长期事实、任务状态和审计。队列消息不能代替可靠的事实数据库。

### 12.7 为什么同时使用向量检索和 BM25？

向量检索擅长语义相似，BM25 擅长精确关键词、故障码和命令。混合检索能覆盖两种情况，再用 RRF 和 Rerank 提高最终排序质量。

### 12.8 为什么 deep 模式使用多个 Agent？

让日志、指标、基础设施和 Runbook 各自负责一种证据，减少上下文干扰，并支持并行取证。最终只把压缩后的 Evidence 写入公共状态。

### 12.9 Evidence 解决什么问题？

提供事实边界、可追溯引用和审计能力，减少 LLM 幻觉，并允许根因判断说明“结论由哪些证据支持”。

### 12.10 Lite Mode 有什么价值？

它不是生产架构替代品，而是本地开发和核心流程验证路径。在缺少完整基础设施时，仍可验证 LangGraph、Embedding、检索、Evidence 和 LLM 报告生成。

---

## 13. 第一遍阅读任务

第一遍只完成以下任务：

1. 能说出项目解决什么问题。
2. 能区分 fast 和 deep。
3. 能说出 FastAPI、LangGraph、Milvus、Redis、PostgreSQL 各自职责。
4. 能解释 RAG 与 Tool 的区别。
5. 能大致复述同步链路和异步链路。
6. 知道源码入口在哪里，不要求现在记住行号。

不要求：

- 背诵所有英文全称。
- 记住全部目录。
- 理解每个数据库细节。
- 立刻读完 deep graph 的全部实现。
- 立刻运行完整 Docker 栈。

---

## 14. 正式学习路线

### 第 1 章：请求如何进入系统

学习：HTTP、FastAPI、Pydantic、Lifespan、SSE、异步生成器。

源码：

```text
app/main.py
app/api/v1/aiops.py
app/schemas/aiops.py
app/services/aiops_service.py
```

### 第 2 章：DiagnosisRunner 与事件流

学习：业务编排、fast/deep 路由、RuntimeEvent、asyncio.Queue、超时和预算。

源码：

```text
app/orchestration/diagnosis_runner.py
app/runtime/stream_sink.py
app/runtime/agent_harness.py
```

### 第 3 章：fast Agent Loop

学习：StateGraph、State、Node、Conditional Edge、Plan-Execute-Replan、死循环。

源码：

```text
app/agents/graph.py
app/agents/state.py
app/agents/skill_router.py
app/agents/planner.py
app/agents/executor.py
app/agents/replanner.py
```

### 第 4 章：Skill 与工具系统

学习：Skill 渐进式披露、工具注册、Tool Call、参数校验、权限和审批。

源码：

```text
app/skills/
app/tools/
app/runtime/tool_runner.py
app/runtime/permissions.py
app/runtime/approvals.py
```

### 第 5 章：RAG 全链路

学习：切分、Embedding、Milvus、BM25、RRF、Rerank、Top-K 和评测。

源码：

```text
app/core/splitter.py
app/core/embedding.py
app/core/hybrid_retriever.py
app/core/reranker.py
app/rag/retrieval.py
scripts/ingest_kb_corpus.py
benchmark/
```

### 第 6 章：deep 多 Agent

学习：专业 Agent、并行 fan-out、Evidence 累加、Reducer、RCA、修复规划。

源码：

```text
app/diagnosis_graphs/deep_diagnosis_graph.py
app/agents/state_deep.py
app/agents/*_agent.py
```

### 第 7 章：Redis、PostgreSQL 与 Worker

学习：队列、消费者组、ACK、重试、DLQ、幂等、事务和审计。

源码：

```text
app/queue/redis_streams.py
app/diagnosis_worker.py
app/db/postgres.py
app/incidents/
app/evidence/
```

### 第 8 章：MCP、Docker 与系统边界

学习：MCP、容器、Compose、Volume、网络、权限模式和高风险工具。

源码：

```text
app/core/mcp_client.py
mcp_servers/
Dockerfile
docker-compose.yml
```

### 第 9 章：失败实验、评测和个人改造

学习：Tool Retry、Context 预算、无 RAG 降级、重复任务、RAG 评测、并发问题。

### 第 10 章：简历和面试

产出：项目描述、1 分钟介绍、3 分钟介绍、架构图、失败案例、个人贡献、追问题库。

---

## 15. 预习结束后的最低目标

看完第一遍，你只要能用自己的话说出下面这段，就达标：

> 这是一个面向运维故障诊断的多 Agent 系统。FastAPI 接收用户问题或告警，DiagnosisRunner 根据请求选择 fast 或 deep 模式。fast 使用 Skill Router、Planner、Executor 和 Replanner 循环排查；deep 会让日志、指标、基础设施和 Runbook Agent 分别收集 Evidence，再进行根因分析和修复规划。系统使用 Milvus 做 RAG 向量检索，Redis Streams 分发后台任务，PostgreSQL 保存任务和证据事实，MCP 接入外部工具，并通过 SSE 把执行过程流式返回给前端。Lite Mode 则用于在个人电脑上低成本验证核心 Agent 和 RAG 链路。

第一遍看不懂全部内容是正常的。正式源码学习会从 `app/main.py` 和一次 HTTP 请求开始，再逐层进入 Agent、RAG、工具、队列和数据库。
