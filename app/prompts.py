"""Prompt composition helpers for both parts of the case."""

from __future__ import annotations

from typing import List


def detect_focus_themes(case_focus: str, subject: str, learning_outcomes: str) -> List[str]:
    """Detect thematic focus from inputs using keyword heuristics."""

    focus_keywords = {
        "innovation": ["innovation", "r&d", "startup", "disruption", "technology", "digital"],
        "financial": ["valuation", "capital", "investment", "financial", "funding", "finance"],
        "strategy": ["strategy", "competitive", "market", "positioning", "business model"],
        "leadership": ["leadership", "management", "culture", "team"],
        "operations": ["operations", "supply chain", "efficiency", "process"],
        "crisis": ["crisis", "turnaround", "emergency", "challenge", "restructuring"],
        "ethics": ["ethics", "responsibility", "compliance", "governance"],
    }
    detected: List[str] = []
    combined_text = f"{case_focus} {subject} {learning_outcomes}".lower()
    for theme, keywords in focus_keywords.items():
        if any(keyword in combined_text for keyword in keywords):
            detected.append(theme)
    return detected


def get_special_sections(focus_themes: List[str]) -> str:
    """Return specialized instruction blocks for detected themes."""

    section_map = {
        "innovation": (
            "\n- Analyze the company's innovation management using frameworks such as "
            "Three Horizons, Build-Buy-Partner decisions, R&D investments, and startup partnerships.\n"
            "- Show clear examples of innovation portfolio management and resource allocation dilemmas.\n"
        ),
        "financial": (
            "\n- Include a deep dive into financial analysis, capital structure, funding rounds, "
            "financial ratios, and comparison with competitors.\n"
        ),
        "strategy": (
            "\n- Evaluate strategic alternatives, market positioning, business model evolution, and partnerships.\n"
        ),
        "leadership": (
            "\n- Describe leadership styles, team dynamics, organizational culture, and decision-making frameworks.\n"
        ),
        "crisis": (
            "\n- Analyze crisis events, turnaround management, stakeholder reactions, and risk mitigation strategies.\n"
        ),
        "ethics": (
            "\n- Include analysis of ethical dilemmas, compliance issues, and corporate governance frameworks.\n"
        ),
    }
    return "".join(section_map[t] for t in focus_themes if t in section_map)


def prompt_part_1(
    subject: str,
    learning_outcomes: str,
    case_focus: str,
    industry_company: str,
    case_type: str,
    financials_table: str,
    facts: str,
) -> str:
    """Compose the first-half prompt for the case generation."""

    focus_themes = detect_focus_themes(case_focus, subject, learning_outcomes)
    extra_sections = get_special_sections(focus_themes)
    if "innovation" in focus_themes:
        frameworks_text = (
            "- Use Three Horizons, Build/Buy/Partner, and innovation portfolio frameworks where relevant."
        )
    elif "financial" in focus_themes:
        frameworks_text = "- Include detailed financial ratio and capital structure analysis."
    elif "strategy" in focus_themes:
        frameworks_text = "- Use frameworks like SWOT, Five Forces, and business model analysis."
    else:
        frameworks_text = ""

    return f"""
You are a top Harvard Business School case writer.

Your task: Write the FIRST HALF of a full, authentic Harvard MBA case (OPENING, COMPANY BACKGROUND, SITUATION DEVELOPMENT) totaling 2500-3500 words, using ONLY real, source-verified facts and the company’s actual financials.

## STRUCTURE & WORD COUNT:
1. **OPENING** (600-800 words)
   - Set the scene: specific time/place, drama, tension, protagonist, dilemma.
   - Show what’s at stake; use character’s inner thoughts and dialogue.
2. **COMPANY BACKGROUND** (1200-1500 words)
   - Founding, growth, evolution, culture, org structure, major milestones.
   - Leadership profiles, strategic pivots, industry, competitors, positioning.
   - Major financial events, funding rounds, investor profiles.
3. **SITUATION DEVELOPMENT** (1000-1200 words)
   - Chronology of events leading to the challenge.
   - Key decisions, external threats, market shifts, internal changes.
   - Reactions of board, management, employees, market.

{extra_sections}
{frameworks_text}

**REQUIREMENTS:**
- Use only the real financial data below (see table).
- All facts, dates, names, numbers, quotes, claims MUST be APA7-cited in-text.
- Use a compelling, vivid Harvard narrative.
- DO NOT go beyond SITUATION DEVELOPMENT — stop after that section.

## INPUTS FOR THIS CASE:
Course: {subject}
Learning Outcomes: {learning_outcomes}
Case Focus: {case_focus}
Company: {industry_company}
Case Type: {case_type}

## FINANCIAL DATA (from Yahoo Finance, millions USD):
{financials_table}

## VERIFIED FACTS AND TIMELINE (from Perplexity):
{facts}

END OF FIRST HALF. (Do not write further sections yet.)
"""


def prompt_part_2(
    subject: str,
    learning_outcomes: str,
    case_focus: str,
    industry_company: str,
    case_type: str,
    financials_table: str,
    facts: str,
    part1_text: str,
) -> str:
    """Compose the second-half prompt for the case generation."""

    focus_themes = detect_focus_themes(case_focus, subject, learning_outcomes)
    extra_sections = get_special_sections(focus_themes)
    if "innovation" in focus_themes:
        frameworks_text = "- Continue using Three Horizons and innovation portfolio frameworks."
    elif "financial" in focus_themes:
        frameworks_text = "- Continue detailed financial ratio and capital structure analysis."
    elif "strategy" in focus_themes:
        frameworks_text = "- Apply SWOT, Five Forces, and business model analysis as relevant."
    else:
        frameworks_text = ""

    return f"""
You are a top Harvard Business School case writer.

Continue the following case with the SECOND HALF. Start with "CENTRAL CHALLENGE" and cover all remaining Harvard MBA case sections, totaling 2500-3500 words.

## STRUCTURE & WORD COUNT:
4. **CENTRAL CHALLENGE** (800-1000 words)
   - All alternatives facing protagonist, pros/cons, stakeholders’ interests, financial/operational constraints. NO solution.
5. **SUPPORTING ANALYSIS** (600-800 words)
   - Quantitative analysis, ratios, benchmarks, SWOT, exhibits reference.
6. **CONCLUSION** (500-600 words)
   - Critical decision moment (cliffhanger). Recap, 5 student discussion questions. NO answer.
7. **EXHIBITS** (6–8 tables/charts, real data, APA7 source)
8. **TEACHING NOTES** (1200–1500 words)
   - Executive summary, learning objectives, teaching plan, questions, sample responses, frameworks.
9. **REFERENCES** (20+ APA7, real sources only)

{extra_sections}
{frameworks_text}

**REQUIREMENTS:**
- Continue in the same style, timeline, narrative and facts as the first half (see below).
- Use only the real financial data below (see table).
- All facts, dates, names, numbers, quotes, claims MUST be APA7-cited in-text.
- Use compelling, vivid Harvard narrative.
- DO NOT recap or repeat previous sections; continue as seamless case.

## CASE PART 1 (reference for consistency):  
{part1_text}

## INPUTS FOR THIS CASE:
Course: {subject}
Learning Outcomes: {learning_outcomes}
Case Focus: {case_focus}
Company: {industry_company}
Case Type: {case_type}

## FINANCIAL DATA (from Yahoo Finance, millions USD):
{financials_table}

## VERIFIED FACTS AND TIMELINE (from Perplexity):
{facts}

**WARNING:**
- This is the final section. Absolutely no solution or answer to the challenge.
- If you lack data for any section, insert “[Not enough data for this section]”.

**BEGIN SECOND HALF.**
"""


