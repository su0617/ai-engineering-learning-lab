# Hello Agents Study Adaptations

This directory contains selected, annotated study adaptations based on Datawhale Hello Agents:

- Source repository: https://github.com/datawhalechina/hello-agents
- Course site: https://hello-agents.datawhale.cc/
- Included modules:
  - chapter01_react_travel_agent: a hand-written Thought-Action-Observation loop;
  - chapter06_langgraph_search: a fixed LangGraph workflow for search question answering.

## What was changed

- Removed all real API keys and local machine paths.
- Unified configuration through the repository-root .env file.
- Added required configuration checks, clearer error handling, and comments aimed at code reading.
- Kept the original learning intent while updating dependency ranges for a current environment.

Only selected adaptations are included. Original course PDFs, large datasets, raw packages, and unmodified files are intentionally excluded.

## Configuration

Copy the repository-root .env.example to .env and fill in your own provider values. Both demos use an OpenAI-compatible LLM endpoint and Tavily web search.

## License and attribution

The source course is licensed under CC BY-NC-SA 4.0. These study adaptations are shared under the same license within this directory. See LICENSE.md for the scope and license link. This notice applies to hello_agent_study only; future independent work under projects may use a different license.

