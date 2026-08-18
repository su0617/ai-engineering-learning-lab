# LangGraph 搜索问答 Workflow

这是使用 LangGraph 实现的搜索问答学习改编，用于理解 State、Node、Edge 和 Checkpoint。

## 图结构

    START
      -> understand
      -> search
      -> answer
      -> END

这是固定 Workflow，不是动态 ReAct Agent。普通请求都会按这三个节点依次执行；动态 Agent 则可以让大模型根据中间结果选择下一个工具或结束任务。

## 核心概念

- SearchState：节点之间共享的数据结构。
- Node：负责一个明确职责的 Python 函数。
- Edge：连接节点并规定执行顺序。
- add_messages：将新消息追加到原列表，而不是覆盖旧消息。
- InMemorySaver：仅在当前进程保存检查点，不是持久化数据库记忆。
- thread_id：标识一条会话检查点。本示例为每个问题生成新的 ID，因此主要表现为单轮搜索问答。

## 节点职责

1. understand：提取用户原问题，让模型生成更适合搜索的关键词。
2. search：使用 Tavily 获取网页信息，并整理成文本证据。
3. answer：基于检索证据组织回答。搜索失败时明确说明信息时效性限制，不编造来源。

## 运行方式

1. 将仓库根目录 .env.example 复制为 .env，并填写自己的配置。
2. 在本目录安装 requirements.txt。
3. 运行 search_workflow.py。
4. 输入问题，输入 quit 退出。

## 改动与局限

- 将原示例依赖个人目录的配置改成仓库根目录 .env。
- 保留真正的用户原问题到 user_query，修正原示例中误保存模型分析结果的问题。
- 增加来源约束提示和 search_failed 分支。
- 有意保持流程固定，便于先观察 LangGraph 的基本结构；后续可继续扩展条件分支、工具调用、持久化和评测。

来源：Datawhale Hello Agents 第六章。许可说明见上级目录的 LICENSE.md。
