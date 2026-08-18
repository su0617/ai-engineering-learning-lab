# ReAct Travel Agent

This is a study adaptation of the Hello Agents Chapter 1 travel assistant. It implements a small ReAct loop by hand instead of relying on an Agent framework.

## What it demonstrates

    User request
        -> LLM Thought and Action
        -> local tool execution
        -> Observation appended to history
        -> LLM decides the next action
        -> Finish or loop limit

Available tools:

- get_weather: requests current weather from wttr.in.
- get_attraction: searches for attraction suggestions with Tavily.

## Key learning points

- available_tools is a dictionary that maps a tool name to a callable Python function.
- prompt_history preserves the current task context. The language model itself has no persistent memory.
- The program parses an Action string, executes the matching tool, then sends the Observation back in the next model call.
- MAX_STEPS is a safety boundary. Without it, an Agent can repeat failed steps and consume time and API cost.

## Run

1. Copy the repository root .env.example to .env and fill in the four variables.
2. Install dependencies from this directory.
3. Run react_travel_agent.py.
4. Enter a travel question, such as: Query the weather in Nanjing today and recommend an attraction.

## Adaptation notes

- Uses the repository-root .env instead of a local file path from the original course folder.
- Does not contain a real API key or a personal machine path.
- Adds timeout handling, early configuration checks, and safer Action parsing.
- This remains a teaching demo. Natural-language parsing with regular expressions is brittle, and a production Agent should use structured tool calling, validation, logging, permissions, and tests.

## Source and license

Based on Datawhale Hello Agents Chapter 1:

- Source: https://github.com/datawhalechina/hello-agents
- License: CC BY-NC-SA 4.0, https://creativecommons.org/licenses/by-nc-sa/4.0/

