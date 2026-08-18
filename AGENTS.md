# 仓库协作说明

这份文件用于承接本仓库后续的 Codex 会话。打开本目录后，请先阅读本文件和根目录 README，再检查 Git 状态。

## 仓库定位

本仓库是 AI 应用工程学习记录与项目展示仓库，面向长期积累和后续求职使用。当前主线是 Python + 大模型应用工程，重点包括：

- Agent、ReAct、工具调用、上下文和记忆；
- LangChain、LangGraph、RAG 和 Workflow；
- FastAPI、MySQL、Docker、评测和可观测性；
- 后续根据真实项目需要考虑模型部署、推理优化和 AI Infra。

仓库不是课程代码压缩包，也不应把照着教程运行的内容包装成完整原创项目。每个学习改编或项目都要尽量写清楚来源、自己的改动、掌握程度、运行方式和局限。

## 本机与远程位置

- 本机唯一长期工作副本：
  D:\Alike_Desktop_Other_Files_suxiaoyong\(对应github仓库，用来简历展示)ai-engineering-learning-lab
- GitHub：
  https://github.com/su0617/ai-engineering-learning-lab
- 默认分支：main
- 老师原始课程资料：
  D:\Alike_Desktop_Other_Files_suxiaoyong\hello_agent_study

课程原始资料目录和 GitHub 仓库目录不要混用。代码、README、学习日志和后续项目改动优先在本仓库完成。

## 当前仓库内容

- hello_agent_study/chapter01_react_travel_agent：
  Hello Agents 第一章手写 ReAct 旅行助手的学习改编。
- hello_agent_study/chapter06_langgraph_search：
  LangGraph 固定搜索 Workflow 的学习改编。
- docs/learning-log.md：
  按时间记录学习内容、阶段产出、掌握情况和后续计划。
- projects/：
  预留给未来独立项目或有实质二次开发的项目。

当前已经完成并推送的提交：

- dc89adf：初始化学习仓库和两个学习示例；
- 2701343：将 README、学习日志和项目说明改为中文。

## 用户的学习特点

- 用户目前以 Python Agent / AI 应用工程为第一方向，未来是否深入 AI Infra 根据实习、课题组任务和实际兴趣再决定。
- 当前阶段以快速扫盲和建立全景认识为主，不要求每个课程 Demo 都逐行默写。
- 重点是理解架构、数据流、模块职责、工程边界，并能对成熟项目进行有意义的二次开发。
- 用户代码阅读能力正在提升，Python 基础和脱离参考独立手写能力仍需在项目中巩固。
- 提供代码时要写必要注释，解释组件用途、输入输出、API 调用位置和容易混淆的逻辑。
- 完成代码不是唯一目的。修改代码时必须同时告诉用户改了什么、为什么改、如何验证，以及仍有哪些局限。

## 环境与磁盘规则

- Python 学习环境优先使用 Conda 环境 agent_study_env。
- 只在真正用到时安装依赖，不要提前一次性配置整套技术栈。
- 不随意修改 base 环境，不批量下载模型，不重复安装已有依赖。
- C 盘空间敏感。课程包、模型、数据集、缓存和大型依赖优先放到 D 盘。
- 运行命令前说明会修改哪个环境、预计影响和是否需要网络。
- 不读取、输出或提交真实 API Key。根目录 .env 被 Git 忽略，只能提交 .env.example。

## 修改仓库的标准流程

1. 先阅读相关 README、代码和学习日志，并检查 git status。
2. 识别用户已有的未提交修改，不覆盖、不回退、不使用 git reset --hard。
3. 先说明准备修改的文件和原因，再使用 apply_patch 做手动编辑。
4. 使用 agent_study_env 做适合风险的语法检查、导入检查或小范围运行测试。
5. 扫描密钥、个人路径、模型文件、数据集和不应提交的缓存。
6. 向用户说明结果、改动、验证结果和剩余风险。
7. 只有用户明确要求同步、提交或推送时，才执行对应 Git 操作。推送前再次检查脱敏和 git diff。

## Git 提交习惯

提交信息使用简洁英文，例如：

- docs: update learning log
- feat: add rag retrieval demo
- fix: handle empty search results

正常同步命令：

    git add .
    git commit -m "说明本次改动"
    git push

不要提交以下内容：

- .env、API Key、密码、Token；
- 原始课程压缩包、PDF、个人绝对路径；
- 模型权重、数据集、向量库、日志和缓存；
- .idea、.vscode、__pycache__ 和本地虚拟环境。

## 后续项目文档要求

未来新增项目时，至少包含：

- 项目背景和要解决的问题；
- 系统架构和主要数据流；
- 使用的模型、工具、存储和部署方式；
- 自己完成的改动，而不是只写“参考开源项目”；
- 运行配置和脱敏说明；
- 测试、评测、已知局限和后续计划。

如果项目主要来自课程或开源仓库，必须保留来源和许可证说明，并在 README 中明确标注学习改编或二次开发范围。
