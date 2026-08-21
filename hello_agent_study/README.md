# Hello Agents 学习改编

本目录记录 Datawhale Hello Agents 的精选学习改编内容。这里保留经过阅读、运行和调整的示例，不上传课程原始压缩包、PDF、大型数据集、密钥或本地运行缓存。

课程来源：

- 源码仓库：https://github.com/datawhalechina/hello-agents
- 课程网站：https://hello-agents.datawhale.cc/

## 当前收录

| 目录 | 内容 | 学习重点 |
| --- | --- | --- |
| chapter01_react_travel_agent | 手写 ReAct 旅行助手 | Thought、Action、Observation、工具注册和循环边界 |
| chapter06_langgraph_search | LangGraph 搜索问答 Workflow | State、Node、Edge、消息和检查点 |
| chapter07_helloagents_framework | 自建 Agent 框架改编 | 统一 LLM 接口、Agent 基类、四种 Agent 范式和工具注册表 |

## 我的改动

- 移除真实 API Key 和个人电脑路径。
- 统一使用仓库根目录的 .env 配置。
- 增加配置检查、异常处理和适合初学者阅读的必要注释。
- 根据当前学习环境调整依赖版本范围。
- 在文档中明确标注课程改编内容与当前局限。
- 第七章保留框架源码，使用 DeepSeek/OpenAI 兼容接口进行适配，并增加无 API 本地自检入口。

## 配置与运行

将仓库根目录的 .env.example 复制为 .env，填写自己的模型服务和 Tavily 配置。两个示例都使用 OpenAI 兼容接口调用模型，并使用 Tavily 搜索网页资料。

具体运行方式、数据流和改动说明见各子目录 README。第七章默认先运行本地计算器自检，显式选择模型模式后才会调用 API。

## 许可说明

本目录内容基于 CC BY-NC-SA 4.0 许可的 Hello Agents。课程来源、署名、非商业使用和相同方式共享要求见 [LICENSE.md](LICENSE.md)。
