# Harvard Case Study Generator (Modular)

A Gradio-based web app that generates Harvard-style MBA case studies using:
- Yahoo Finance (financials via `yfinance`)
- Perplexity (fact collection)
- Anthropic Claude (long-form generation)

This refactor introduces a clean, PEP8-compliant, modular architecture for easier maintenance and experimentation with multiple LLM providers.

## Features
- Password-gated UI
- Automatic theme detection (innovation/finance/strategy/etc.) with extra instructions
- Yahoo Finance data ingestion and simple tabular formatting
- Perplexity research query for timeline/facts/sources
- Two-step LLM generation (Part 1 and Part 2 of the case)
- Lightweight quality checks
- Download generated case as `.txt`

## Project Structure
```
app/
  __init__.py
  anthropic_client.py    # Claude API wrapper
  config.py              # Env and config loading
  finance.py             # Ticker + financial statements via yfinance
  main.py                # Entrypoint (python -m app.main)
  perplexity.py          # Perplexity API wrapper
  prompts.py             # Prompt composition helpers
  quality.py             # Heuristic quality checks
  service.py             # Orchestrates data + LLM calls
  ui.py                  # Gradio UI
Procfile                  # web: python -m app.main
requirements.txt
README.md
```

## Requirements
- Python 3.10+
- `pip install -r requirements.txt`

## Environment Variables
Create a `.env` file (or set these in your hosting provider):
```
PERPLEXITY_API_KEY=...
CLAUDE_API_KEY=...
CASEGEN_PASSWORD=ksegbs123
HOST=0.0.0.0
PORT=7860
```

You can copy from `.env.example` if present.

## Running Locally
```bash
pip install -r requirements.txt
python -m app.main
```
Open the printed URL, enter the password, and generate a case.

## Deploy
- Heroku/Render/Railway: the provided `Procfile` uses `web: python -m app.main`.
- Set the environment variables in your hosting dashboard.

## Customization
- Swap LLMs: extend `anthropic_client.py` or add a new client module (e.g., Gemini) and make the `service.py` use it behind a configuration switch.
- Adjust prompts: edit `app/prompts.py`.
- Extend quality checks: update `app/quality.py`.

## Security Notes
- Never commit real API keys. Use `.env` locally and provider secrets in production.
- Keep `CASEGEN_PASSWORD` strong and rotate as needed.

## License
Proprietary
