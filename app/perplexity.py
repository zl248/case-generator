"""Perplexity API client wrapper."""

from __future__ import annotations

import requests
from typing import Optional


PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


def build_research_query(
    subject: str,
    learning_outcomes: str,
    case_focus: str,
    industry_company: str,
    case_type: str,
    specialized_sections: str,
) -> str:
    """Compose a data-collection prompt for Perplexity."""

    return f"""
COMPREHENSIVE DATA COLLECTION for Harvard Business School case study

COMPANY: {industry_company}
CASE TYPE: {case_type}
FOCUS: {case_focus}

{specialized_sections}

1. Exact timeline, key events and decisions (with dates)
2. Company/industry verified facts, primary and secondary sources (URLs, authors, date)
3. Key people, stakeholders, decision makers (with background)
4. Financial/market data (with sources)
5. Market, competition, and regulatory context
6. Strategic and operational details
7. Harvard-style references in APA7

Format as numbered, source-attributed facts (not narrative).
"""


def search_perplexity(
    api_key: Optional[str],
    query: str,
) -> str:
    """Execute a Perplexity chat completion request and return text content."""

    if not api_key:
        return "No data found. (Missing PERPLEXITY_API_KEY)"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "sonar",
        "messages": [{"role": "user", "content": query}],
    }
    response = requests.post(PERPLEXITY_URL, headers=headers, json=body)
    data = response.json()
    if "choices" in data and data["choices"]:
        return data["choices"][0]["message"]["content"]
    return "No data found."


