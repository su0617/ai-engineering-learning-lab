# 学习日志

这份日志用于记录学习时间、学习内容、实际产出、掌握程度和下一步计划。后续每完成一个阶段，就在这里补充一条，而不是只记录“看完了某门课”。

## 2026 年 7 月：LangChain 基础

学习内容：

- 模型调用、消息、Prompt 和 Chain。
- 字符串、列表、JSON、Pydantic 等输出解析。
- 文档加载、文本切分、Embedding、向量库、Retriever 和基础 RAG。
- Agent、工具调用和 ReAct 的基本概念。

阶段收获：

- 能够说明主要组件的职责和输入输出。
- 能够描述基础 RAG 和 Agent 的完整数据流。
- 能够区分固定 Chain / Workflow 与动态 Agent。

## 2026 年 7 月：Hello Agents 第一章

学习内容：

- Agent 的定义、分类和 PEAS 任务环境。
- 手写 Thought-Action-Observation 循环。
- 工具注册、工具执行、Observation 回传、Finish 和循环上限。
- 记忆、系统 1 / 系统 2、幻觉和 Agent 评估。

阶段产出：

- 完成一个手写 ReAct 旅行助手的学习改编。
- 将课程代码改为读取统一环境配置，移除本地路径和真实密钥。
- 增加必要的配置检查、异常处理和学习注释。

掌握情况：

- 能够结合代码讲清主要流程和关键变量。
- 暂时不能完全脱离参考从零手写全部代码，Python 字典、函数对象、参数解析和第三方 API 返回结构仍在项目中继续巩固。

## 2026 年 8 月初：Agent 与大模型基础扫盲

学习内容：

- Agent 技术发展背景。
- 大模型、Token、上下文、Prompt、采样参数和幻觉。
- 模型能力边界、工具调用和 Workflow / Agent 的适用场景。

学习策略：

- 当前阶段先建立全景认识，不为逐行复现每个 Demo 停留过久。
- Transformer、注意力机制和 PyTorch 的深入学习放在李沐课程中低占比推进。

## 2026 年 8 月：LangGraph

阶段产出：

- 完成一个“理解问题 → 搜索资料 → 组织回答”的 LangGraph 固定 Workflow。
- 学习 State、Node、Edge、消息追加和 InMemorySaver。
- 修正示例中用户原问题保存错误的问题，并增加搜索失败分支和来源约束提示。

当前认识：

- 能够说明 LangGraph 如何把流程显式组织成图。
- 能够区分本示例的固定 Workflow 与动态 ReAct Agent。
- 后续需要在更复杂的分支、持久化、工具调用和评测中继续深入。

## 2026 年 9 月：上下文工程与代码库维护助手

阶段产出：

- 完成 Datawhale Hello-Agents 第九章 `codebase_maintainer.py` 的学习改编整理。
- 梳理 ContextBuilder、NoteTool、TerminalTool、MemoryTool 与 FunctionCallAgent 的组合关系。
- 将演示项目名和代码库路径改为通用相对值，并补充运行产物忽略规则。

当前边界：

- 本次只进行源码脱敏和文档整理，没有安装依赖或启动外部服务。
- 代码仍属于课程学习改编，尚未进行完整兼容性验证和生产级权限、评测改造。

## 下一阶段

- 继续学习 LangGraph，并结合 Agent Harness 相关项目理解工程机制。
- 选择成熟 RAG / Agent 项目做架构分析和有意义的二次开发。
- 根据真实项目需要补充 FastAPI、MySQL、Docker、评测和可观测性。
