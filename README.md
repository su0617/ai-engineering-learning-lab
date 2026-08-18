# LLM Agent Learning Lab

This repository records my learning and hands-on adaptations for LLM application engineering. It is not a collection of raw course files. Each included example is selected because I can explain its architecture, data flow, limitations, and possible extensions.

My current focus is Python-based Agent and RAG application development. The learning path starts with Agent fundamentals and LangGraph, then moves toward project adaptation, evaluation, API services, and deployment.

## Current scope

| Area | Status | What I can explain |
| --- | --- | --- |
| LangChain fundamentals | Completed | prompts, chains, structured output, retrieval basics, and tool calling |
| ReAct Agent | Completed study demo | Thought-Action-Observation loop, tool registry, parsing, loop boundaries |
| LangGraph | In progress | State, Node, Edge, checkpointing, and fixed workflow design |
| Independent projects | Planned | RAG/Agent project adaptation, FastAPI, MySQL, Docker, evaluation |

## Repository map

    .
    |-- hello_agent_study/
    |   |-- chapter01_react_travel_agent/
    |   |-- chapter06_langgraph_search/
    |-- docs/
    |   |-- learning-log.md
    |-- projects/
    |-- .env.example
    |-- .gitignore
    +-- README.md

The hello_agent_study directory contains selected study adaptations based on the Hello Agents open-source course. The projects directory is reserved for future independent or substantially reworked projects.

## Running a demo

1. Create a Python environment for this repository.
2. Copy .env.example to .env and fill in your own API keys.
3. Install the requirements in the chosen demo directory.
4. Run the corresponding Python file.

Never commit .env, API keys, model files, datasets, or original course packages.

## Attribution

The materials in hello_agent_study are study adaptations based on Datawhale Hello Agents. They retain the required attribution and non-commercial share-alike notice. See hello_agent_study/README.md and hello_agent_study/LICENSE.md.

## Learning principle

At this stage I prioritize understanding the system: what enters a module, what leaves it, why a design is chosen, and where it can fail. For future portfolio projects, I will deepen code-level implementation, testing, evaluation, service APIs, persistence, and deployment around real requirements.

