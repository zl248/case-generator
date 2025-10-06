"""Configuration and environment handling for the application.

Loads environment variables and exposes typed accessors for API keys,
application password, and server configuration.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Immutable app configuration container."""

    perplexity_api_key: Optional[str]
    claude_api_key: Optional[str]
    access_password: str
    host: str
    port: int


def get_config() -> AppConfig:
    """Create configuration from environment variables.

    Returns:
        AppConfig: Populated configuration object.
    """

    perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    access_password = os.getenv("CASEGEN_PASSWORD", "ksegbs123")
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "7860"))

    return AppConfig(
        perplexity_api_key=perplexity_api_key,
        claude_api_key=claude_api_key,
        access_password=access_password,
        host=host,
        port=port,
    )


