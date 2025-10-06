"""Lightweight quality checks for generated case text."""

from __future__ import annotations

from typing import List


def quick_quality_check(case_text: str, focus_themes: List[str]) -> str:
    """Run a few heuristic checks on the generated case text."""

    checks = {
        "APA citations": ("(" in case_text and ")" in case_text),
        "Framework mentioned": any(theme in case_text.lower() for theme in focus_themes),
        "Exhibits": ("exhibit" in case_text.lower() or "таблиця" in case_text.lower()),
        "Finance present": ("$" in case_text or "million" in case_text.lower()),
    }
    missing = [name for name, ok in checks.items() if not ok]
    if not missing:
        return "✅ Case passes core quality checks!"
    return "⚠️ Missing: " + ", ".join(missing)


