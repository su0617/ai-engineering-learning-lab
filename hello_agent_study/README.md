# Hello Agents 学习改编

本目录记录 Datawhale Hello Agents 的精选学习改编内容。这里保留的是经过理解、运行和调整的示例，不上传课程原始压缩包、PDF、大型数据集或未改动的全部源码。

课程来源：

- 源码仓库：https://github.com/datawhalechina/hello-agents
- 课程网站：https://hello-agents.datawhale.cc/

## 当前收录

| 目录 | 内容 | 学习重点 |
| --- | --- | --- |
| chapter01_react_travel_agent | 手写 ReAct 旅行助手 | Thought、Action、Observation、工具注册和循环边界 |
| chapter06_langgraph_search | LangGraph 搜索问答 Workflow | State、Node、Edge、消息和检查点 |

## 我的改动

- 移除真实 API Key 和个人电脑路径。
- 统一使用仓库根目录的 .env 配置。
- 增加配置检查、异常处理和适合初学者阅读的必要注释。
- 根据当前学习环境调整依赖版本范围。
- 在文档中明确标注课程改编内容与当前局限。

## 配置与运行

将仓库根目录的 .env.example 复制为 .env，填写自己的模型服务和 Tavily 配置。两个示例都使用 OpenAI 兼容接口调用模型，并使用 Tavily 搜索网页资料。

具体运行方式、数据流和改动说明见各子目录 README。

## 许可说明

本目录内容基于 CC BY-NC-SA 4.0 许可的 Hello Agents。课程来源、署名、非商业使用和相同方式共享要求见 [LICENSE.md](LICENSE.md)。
