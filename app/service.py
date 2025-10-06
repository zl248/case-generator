"""Application service orchestrating data fetches and LLM calls."""

from __future__ import annotations

from typing import List

from .config import AppConfig
from .finance import extract_ticker, get_financial_data_yf, format_financials_table
from .perplexity import build_research_query, search_perplexity
from .prompts import detect_focus_themes, prompt_part_1, prompt_part_2
from .anthropic_client import call_claude
from .quality import quick_quality_check


def generate_harvard_case_2api(
    config: AppConfig,
    subject: str,
    learning_outcomes: str,
    case_focus: str,
    industry_company: str,
    case_type: str,
) -> str:
    """Generate a full Harvard-style case using Perplexity + Anthropic."""

    try:
        ticker = extract_ticker(industry_company)
        financial_data_yf = get_financial_data_yf(ticker) if ticker else {}
        financials_table = format_financials_table(financial_data_yf)

        focus_themes: List[str] = detect_focus_themes(case_focus, subject, learning_outcomes)

        research_query = build_research_query(
            subject,
            learning_outcomes,
            case_focus,
            industry_company,
            case_type,
            "",
        )
        facts = search_perplexity(config.perplexity_api_key, research_query)

        prompt1 = prompt_part_1(
            subject,
            learning_outcomes,
            case_focus,
            industry_company,
            case_type,
            financials_table,
            facts,
        )
        part1_text = call_claude(config.claude_api_key, prompt1)

        prompt2 = prompt_part_2(
            subject,
            learning_outcomes,
            case_focus,
            industry_company,
            case_type,
            financials_table,
            facts,
            part1_text,
        )
        part2_text = call_claude(config.claude_api_key, prompt2)

        case_text = part1_text.strip() + "\n\n" + part2_text.strip()
        word_count = len(case_text.split())
        quality_report = quick_quality_check(case_text, focus_themes)
        case_text += f"\n\n[Word count: {word_count}]\n{quality_report}"
        return case_text
    except Exception as exc:  # pragma: no cover - defensive
        return f"Error during case generation: {str(exc)}"


