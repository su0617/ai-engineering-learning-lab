# 第九章：上下文工程与代码库维护助手

> 学习改编时间：2026-09-10

本目录同步 Datawhale `Hello-Agents` 第九章中的 `codebase_maintainer.py`，用于理解上下文构建、结构化笔记、终端访问、工作记忆和 Agentic 工具决策如何组合成一个长程代码库维护助手。

## 文件说明

| 文件 | 内容 |
| --- | --- |
| `codebase_maintainer.py` | 代码库维护助手核心实现 |
| `.gitignore` | 忽略运行时生成的笔记目录和会话报告 |

## 核心数据流

```text
用户问题
    ↓
检索相关笔记
    ↓
ContextBuilder 构建上下文
    ↓
FunctionCallAgent 自主选择工具
    ├── TerminalTool：探索代码库
    ├── NoteTool：记录发现和任务
    └── MemoryTool：保存工作记忆
    ↓
更新对话历史与会话统计
```

## 本次学习改编与脱敏

- 保留课程示例的主要类、工具注册和 Agentic 执行流程，便于与原教程对照阅读。
- 将演示中的项目名改为通用的 `demo_project`，将代码库路径改为 `./demo_project` 相对路径。
- 没有保留 API Key、Token、个人绝对路径、真实项目名称或本地运行数据。
- 增加中文说明，明确笔记和报告属于运行时产物，不应提交到仓库。
- 本次只做源码脱敏和文档整理，没有安装依赖，也没有进行兼容性改造或完整运行验证。

## 运行提示

该示例依赖 Datawhale Hello-Agents 第九章对应的 `hello_agents` 组件和模型配置。运行前需要准备课程要求的依赖及环境变量；本次同步没有额外安装任何依赖。

```powershell
python codebase_maintainer.py
```

示例默认使用相对路径 `./demo_project` 作为待维护代码库，运行时可能生成 `demo_project_notes/` 和 `maintainer_report_*.json`，这些文件已通过本目录 `.gitignore` 忽略。

## 当前局限

- 这是课程学习改编，不是独立生产级代码库维护系统。
- 工具权限、命令白名单、模型输出校验、持久化记忆和评测仍依赖上游组件或后续工程化改造。
- 本次未安装依赖、未启动外部服务，也未调用真实模型 API。

来源：[Datawhale Hello-Agents 第九章](https://github.com/datawhalechina/hello-agents/tree/main/code/chapter9)。
许可说明见上级目录的 [LICENSE.md](../LICENSE.md)。
