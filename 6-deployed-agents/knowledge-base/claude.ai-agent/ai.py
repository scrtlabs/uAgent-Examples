import json
import os
from typing import Any

import requests

CLAUDE_URL = "https://api.anthropic.com/v1/messages"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY")
if ANTHROPIC_API_KEY is None or ANTHROPIC_API_KEY == "YOUR_ANTHROPIC_API_KEY":
    raise ValueError(
        "You need to provide an API key: https://platform.openai.com/api-keys"
    )
MODEL_ENGINE = os.getenv("MODEL_ENGINE", "claude-3-haiku-20240307")
HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

# "claude-3-5-sonnet-20240620",  # Most intelligent model
# "claude-3-opus-20240229",  # Excels at writing and complex tasks
# "claude-3-sonnet-20240229",  # Balance of speed and intelligence
# "claude-3-haiku-20240307",  # Fast & cost-effective


def create_structured_response_tool(
    response_model_schema: dict[str, Any]
) -> dict[str, Any]:

    # Exclude the title from the schema (not allowed in the API)
    for data in response_model_schema["properties"].values():
        if "title" in data:
            data.pop("title")

    return {
        "name": response_model_schema["title"],
        "description": response_model_schema.get("description", ""),
        "input_schema": response_model_schema,
    }


# Send a prompt to the AI model and return the content of the completion
def get_completion(prompt: str, tool: dict[str, Any] | None = None) -> str | None:
    data = {
        "model": MODEL_ENGINE,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
    }
    if tool:
        data["tools"] = [tool]
        data["tool_choice"] = {"type": "tool", "name": tool["name"]}

    try:
        response = requests.post(
            CLAUDE_URL, headers=HEADERS, data=json.dumps(data), timeout=120
        )
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

    if tool:
        for item in response.json()["content"]:
            if item["type"] == "tool_use":
                return item["input"]

    messages = response.json()["content"]
    message = messages[0]["text"]
    return message


def get_structured_response(
    prompt: str, response_model_schema: dict[str, Any]
) -> dict[str, Any] | None:
    tool = create_structured_response_tool(response_model_schema)
    return get_completion(prompt, tool)
