"""Top-level package for the Harvard Case Generator app.

This package provides a modular, testable structure for:
- configuration and environment handling
- financial data retrieval from Yahoo Finance
- data/facts retrieval from Perplexity
- LLM interaction (Anthropic Claude)
- prompt composition
- quality checks
- Gradio UI composition and app entrypoint

All modules follow PEP8 and include type hints and concise docstrings.
"""

__all__ = [
    "config",
    "finance",
    "perplexity",
    "anthropic_client",
    "prompts",
    "quality",
    "service",
    "ui",
]


