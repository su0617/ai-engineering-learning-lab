"""
LangGraph search workflow.

The graph is fixed: understand -> search -> answer.
It is useful for learning State, Node, Edge, and checkpointing before adding
dynamic branching or tool-calling Agent behavior.
"""

import asyncio
import os
from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from tavily import TavilyClient


REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"
load_dotenv(ENV_PATH)


class SearchState(TypedDict):
    """The shared state passed from one LangGraph node to the next."""

    # New messages are appended, so previous messages remain observable.
    messages: Annotated[list, add_messages]
    user_query: str
    search_query: str
    search_results: str
    final_answer: str
    step: str


def require_env(name: str) -> str:
    """Fail early with a clear message when a required setting is absent."""

    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable {name}. Check {ENV_PATH}.")
    return value


llm = ChatOpenAI(
    model=require_env("GUAIHUB_MODEL"),
    api_key=require_env("GUAIHUB_API_KEY"),
    base_url=require_env("GUAIHUB_BASE_URL"),
    temperature=0.2,
)
tavily_client = TavilyClient(api_key=require_env("TAVILY_API_KEY"))


def message_text(content: object) -> str:
    """Normalize a message content value for prompts and state fields."""

    return content if isinstance(content, str) else str(content)


def understand_query_node(state: SearchState) -> dict:
    """Node 1: turn a natural-language question into a web-search query."""

    user_query = next(
        (
            message_text(message.content)
            for message in reversed(state["messages"])
            if isinstance(message, HumanMessage)
        ),
        "",
    )

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You generate search queries. Reply in Chinese with exactly two lines: "
                    "Understanding: a concise request summary; "
                    "Search query: precise web search keywords."
                )
            ),
            HumanMessage(content=user_query),
        ]
    )
    response_text = message_text(response.content)
    search_query = user_query
    if "Search query:" in response_text:
        search_query = response_text.split("Search query:", 1)[1].strip()

    return {
        # Keep the original user question for the final answer node.
        "user_query": user_query,
        "search_query": search_query,
        "step": "understood",
        "messages": [AIMessage(content=f"Understanding stage:\n{response_text}")],
    }


def tavily_search_node(state: SearchState) -> dict:
    """Node 2: retrieve current web information with Tavily."""

    try:
        print(f"Searching: {state['search_query']}")
        response = tavily_client.search(
            query=state["search_query"],
            search_depth="basic",
            include_answer=True,
            include_raw_content=False,
            max_results=5,
        )
    except Exception as error:
        error_text = f"Search failed: {error}"
        print(error_text)
        return {
            "search_results": error_text,
            "step": "search_failed",
            "messages": [AIMessage(content="Search failed; the final answer will state its limitation.")],
        }

    evidence: list[str] = []
    if response.get("answer"):
        evidence.append(f"Search summary:\n{response['answer']}")

    for index, result in enumerate(response.get("results", [])[:3], start=1):
        evidence.append(
            f"{index}. {result.get('title', 'Untitled')}\n"
            f"{result.get('content', '')}\n"
            f"Source: {result.get('url', '')}"
        )

    result_text = "\n\n".join(evidence) if evidence else "No search results were found."
    return {
        "search_results": result_text,
        "step": "searched",
        "messages": [AIMessage(content="Search stage completed. Preparing an evidence-grounded answer.")],
    }


def generate_answer_node(state: SearchState) -> dict:
    """Node 3: compose a cautious answer based on retrieved evidence."""

    if state["step"] == "search_failed":
        prompt = (
            "Web search is unavailable. Answer the user cautiously, clearly say that "
            "the information may not be current, and do not invent sources.\n\n"
            f"User question: {state['user_query']}"
        )
    else:
        prompt = (
            "Answer the user in Chinese using only the supplied search evidence. "
            "Keep the structure clear, attach source URLs to important factual claims, "
            "and state when the evidence is insufficient. Do not turn speculation into fact.\n\n"
            f"User question: {state['user_query']}\n\n"
            f"Search evidence:\n{state['search_results']}"
        )

    response = llm.invoke(
        [
            SystemMessage(content="You are a rigorous Chinese search question-answering assistant."),
            HumanMessage(content=prompt),
        ]
    )
    final_answer = message_text(response.content)
    return {
        "final_answer": final_answer,
        "step": "completed",
        "messages": [AIMessage(content=final_answer)],
    }


def create_search_workflow():
    """Build the graph by registering nodes and their fixed execution edges."""

    workflow = StateGraph(SearchState)
    workflow.add_node("understand", understand_query_node)
    workflow.add_node("search", tavily_search_node)
    workflow.add_node("answer", generate_answer_node)

    workflow.add_edge(START, "understand")
    workflow.add_edge("understand", "search")
    workflow.add_edge("search", "answer")
    workflow.add_edge("answer", END)

    # In-memory checkpoints disappear when this Python process exits.
    return workflow.compile(checkpointer=InMemorySaver())


async def main() -> None:
    app = create_search_workflow()
    print("LangGraph search workflow started. Type quit to exit.")

    session_count = 0
    while True:
        user_input = input("\nQuestion: ").strip()
        if user_input.lower() in {"quit", "q", "exit"}:
            break
        if not user_input:
            continue

        session_count += 1
        config = {"configurable": {"thread_id": f"search-session-{session_count}"}}
        initial_state: SearchState = {
            "messages": [HumanMessage(content=user_input)],
            "user_query": "",
            "search_query": "",
            "search_results": "",
            "final_answer": "",
            "step": "start",
        }

        try:
            async for event in app.astream(initial_state, config=config):
                for node_name, node_output in event.items():
                    latest_messages = node_output.get("messages", [])[-1:]
                    if not latest_messages:
                        continue
                    print(f"\n[{node_name}]\n{message_text(latest_messages[0].content)}")
        except Exception as error:
            print(f"Workflow failed: {error}")


if __name__ == "__main__":
    asyncio.run(main())
