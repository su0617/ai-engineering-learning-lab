"""
Hand-written ReAct travel assistant.

This example is intentionally small. Its purpose is to show the loop:
Thought -> Action -> Observation -> next Thought.
"""

import os
import re
from pathlib import Path
from typing import Callable

import requests
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient


# Both study demos use one root-level configuration file, which is ignored by Git.
REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"
load_dotenv(ENV_PATH)

MAX_STEPS = 5

AGENT_SYSTEM_PROMPT = """
You are a Chinese travel assistant. Solve the user's request step by step with tools.

Available tools:
- get_weather(city="city name"): query current weather.
- get_attraction(city="city name", weather="weather description"): search attractions.

For every response, output exactly one Thought and one Action:
Thought: your brief reasoning and next plan
Action: function_name(arg_name="arg_value") or Finish[final answer]

Use one tool at a time. When enough information has been collected, use Finish.
"""


def require_env(name: str) -> str:
    """Return a required setting or fail before any paid API call happens."""

    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable {name}. Check {ENV_PATH}.")
    return value


def get_weather(city: str) -> str:
    """Query wttr.in and turn its JSON response into a short observation."""

    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10,
            headers={"User-Agent": "llm-agent-learning-lab/1.0"},
        )
        response.raise_for_status()
        current = response.json()["current_condition"][0]
        description = current["weatherDesc"][0]["value"]
        temperature = current["temp_C"]
        return f"{city} current weather: {description}, {temperature} C."
    except requests.RequestException as error:
        return f"Weather request failed: {error}"
    except (KeyError, IndexError, ValueError) as error:
        return f"Weather response parsing failed: {error}"


def get_attraction(city: str, weather: str) -> str:
    """Use Tavily to retrieve attraction ideas that match the observed weather."""

    tavily = TavilyClient(api_key=require_env("TAVILY_API_KEY"))
    query = f"Best attractions in {city} for {weather} weather, with reasons"

    try:
        response = tavily.search(
            query=query,
            search_depth="basic",
            include_answer=True,
            max_results=3,
        )
    except Exception as error:
        return f"Attraction search failed: {error}"

    if response.get("answer"):
        return response["answer"]

    results = response.get("results", [])
    if not results:
        return "No attraction information was found."

    return "\n".join(
        f"- {item.get('title', 'Untitled')}: {item.get('content', '')}"
        for item in results
    )


# The Agent chooses a string name; this registry turns it into a Python function.
TOOLS: dict[str, Callable[..., str]] = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}


class OpenAICompatibleClient:
    """Small adapter for providers exposing an OpenAI-compatible chat endpoint."""

    def __init__(self) -> None:
        self.model = require_env("GUAIHUB_MODEL")
        self.client = OpenAI(
            api_key=require_env("GUAIHUB_API_KEY"),
            base_url=require_env("GUAIHUB_BASE_URL"),
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": AGENT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        return response.choices[0].message.content or ""


def parse_action(llm_output: str) -> tuple[str, dict[str, str]] | None:
    """Parse one Action line into a tool name and keyword arguments.

    The regular expression is deliberate teaching code, not production-grade parsing.
    """

    action_match = re.search(r"^Action:\s*(.+)$", llm_output, re.MULTILINE)
    if not action_match:
        return None

    action = action_match.group(1).strip()
    if action.startswith("Finish[") and action.endswith("]"):
        return "Finish", {"answer": action[7:-1].strip()}

    tool_match = re.fullmatch(r"(\w+)\((.*)\)", action)
    if not tool_match:
        return None

    tool_name, raw_arguments = tool_match.groups()
    arguments = dict(re.findall(r'(\w+)="([^"]*)"', raw_arguments))
    return tool_name, arguments


def run_agent(user_request: str) -> None:
    """Run the Thought-Action-Observation loop for one user request."""

    llm = OpenAICompatibleClient()
    prompt_history = [f"User request: {user_request}"]

    for step in range(1, MAX_STEPS + 1):
        print(f"\n--- Step {step}/{MAX_STEPS} ---")
        llm_output = llm.generate("\n".join(prompt_history)).strip()
        print(f"Model output:\n{llm_output}")
        prompt_history.append(llm_output)

        parsed_action = parse_action(llm_output)
        if parsed_action is None:
            observation = "Action parsing failed. Follow the required Action format."
        else:
            tool_name, arguments = parsed_action
            if tool_name == "Finish":
                print(f"\nFinal answer:\n{arguments['answer']}")
                return
            if tool_name not in TOOLS:
                observation = f"Unknown tool: {tool_name}"
            else:
                try:
                    observation = TOOLS[tool_name](**arguments)
                except TypeError as error:
                    observation = f"Tool arguments are invalid: {error}"

        observation_text = f"Observation: {observation}"
        print(observation_text)
        prompt_history.append(observation_text)

    print("\nStopped because the maximum number of steps was reached.")


if __name__ == "__main__":
    request = input("Enter a travel request: ").strip()
    if request:
        run_agent(request)
