# LangGraph Search Workflow

This study adaptation implements a small search question-answering workflow with LangGraph.

## Graph structure

    START
      -> understand
      -> search
      -> answer
      -> END

This is a fixed Workflow, not a dynamic ReAct Agent. Every normal request follows the same three nodes. A ReAct Agent would let the model repeatedly choose the next tool or decide to finish.

## Core concepts

- SearchState: the shared data structure that nodes read and update.
- Node: a Python function that performs one clear responsibility.
- Edge: an explicit connection that decides which node runs next.
- add_messages: appends new messages instead of replacing the old message list.
- InMemorySaver: a checkpoint store for this process only. It is not durable database memory.
- thread_id: identifies a conversation checkpoint. In this demo every new query receives its own id, so it behaves as single-turn search question answering.

## Node responsibilities

1. understand: extracts the raw user question and asks the LLM to generate a concise search query.
2. search: sends that query to Tavily and converts results into plain text evidence.
3. answer: uses only the provided evidence to generate a cautious answer. If search fails, it states the freshness limitation instead of inventing sources.

## Run

1. Copy the repository root .env.example to .env and fill in the values.
2. Install the requirements in this directory.
3. Run search_workflow.py.
4. Enter a question. Type quit to exit.

## Adaptation notes

- Reads the repository-root .env rather than a personal local path.
- Preserves the original user question in user_query. It does not mistakenly save the LLM analysis there.
- Adds source-aware answer prompts and an explicit search_failed path.
- Keeps the graph fixed on purpose so State, Node, Edge, and checkpointing remain easy to observe.

## Source and license

Based on Datawhale Hello Agents Chapter 6:

- Source: https://github.com/datawhalechina/hello-agents
- License: CC BY-NC-SA 4.0, https://creativecommons.org/licenses/by-nc-sa/4.0/

