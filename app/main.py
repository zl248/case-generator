"""Application entrypoint for running the Gradio server."""

from __future__ import annotations

from .config import get_config
from .ui import build_app


def run() -> None:
    config = get_config()
    app = build_app()
    app.launch(server_name=config.host, server_port=config.port)


if __name__ == "__main__":
    run()


