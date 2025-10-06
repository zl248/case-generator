"""Anthropic Claude API client wrapper."""

from __future__ import annotations

from typing import Optional

import requests


ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"


def call_claude(
    api_key: Optional[str],
    prompt: str,
    *,
    model: str = "claude-3-opus-20240229",
    max_tokens: int = 4096,
    temperature: float = 0.5,
) -> str:
    """Call Anthropic Claude messages endpoint and return consolidated text."""

    if not api_key:
        return "API Error: Missing CLAUDE_API_KEY"

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(ANTHROPIC_URL, headers=headers, json=body)
    if response.status_code != 200:
        return f"API Error: {response.status_code}. Response: {response.text[:500]}"
    data = response.json()
    contents = data.get("content")
    if isinstance(contents, list):
        result = ""
        for item in contents:
            if item.get("type") == "text":
                result += item.get("text", "")
        return result
    if isinstance(contents, str):
        return contents
    return "No data returned from Claude."


