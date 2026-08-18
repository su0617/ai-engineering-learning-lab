# ReAct 旅行助手

这是基于 Hello Agents 第一章的学习改编，用较少的代码手写一个 ReAct 循环，不依赖 Agent 框架。

## 运行流程

    用户问题
        -> 大模型生成 Thought 和 Action
        -> 程序执行工具
        -> 将结果作为 Observation 加回历史
        -> 大模型决定下一步
        -> Finish 或达到循环上限

当前有两个工具：

- get_weather：调用 wttr.in 查询天气。
- get_attraction：调用 Tavily 搜索景点建议。

## 学习重点

- 工具注册表是一个字典，将模型生成的工具名映射到 Python 函数。
- prompt_history 保存当前任务上下文，大模型接口本身不会自动记忆历史。
- 程序解析 Action，调用对应工具，再把 Observation 传给下一轮模型请求。
- MAX_STEPS 是安全边界，防止模型重复失败、浪费时间和 API 费用。

## 运行方式

1. 将仓库根目录 .env.example 复制为 .env，并填写自己的配置。
2. 在本目录安装 requirements.txt。
3. 运行 react_travel_agent.py。
4. 输入类似“查询今天南京天气，并推荐一个适合游玩的景点”的问题。

## 改动与局限

- 将原课程中依赖个人目录的配置方式改成仓库根目录 .env。
- 移除真实密钥和个人电脑路径。
- 增加超时处理、配置检查和更稳妥的 Action 解析。
- 这是学习 Demo。正则解析自然语言存在脆弱性，生产系统还需要结构化工具调用、参数校验、日志、权限控制和测试。

来源：Datawhale Hello Agents 第一章。许可说明见上级目录的 LICENSE.md。
